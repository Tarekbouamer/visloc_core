import re
import sys
from collections import defaultdict
from copy import deepcopy

__all__ = ['list_models', 'is_model', 'model_entrypoint',
           'list_modules', 'is_model_in_modules', 'is_model_pretrained']


# dict of sets to check membership of model in module
_module_to_models = defaultdict(set)
_model_to_module = {}                   # mapping of model names to module names
_model_entrypoints = {}                 # mapping of model names to entrypoint fns
# set of model names that have pretrained weight url present
_model_has_pretrained = set()
_model_pretrained_cfgs = dict()         # central repo for model default_cfgs


def is_model(model_name):
    """ Check if a model name exists """
    return model_name in _model_entrypoints


def model_entrypoint(model_name):
    """ Fetch a model entrypoint for specified model name """
    return _model_entrypoints[model_name]


def list_modules():
    """ Return list of module names that contain models / model entrypoints"""
    modules = _module_to_models.models.keys()
    return list(sorted(modules))


def is_model_in_modules(model_name, module_names):
    """ Check if a model exists within a subset of modules
        model_name (str) - name of model to check
        module_names (tuple, list, set) - names of modules to search in
    """
    assert isinstance(module_names, (tuple, list, set))
    return any(model_name in _module_to_models[n] for n in module_names)


def is_model_pretrained(model_name):
    return model_name in _model_has_pretrained


def get_pretrained_cfg(model_name):
    if model_name in _model_pretrained_cfgs:
        return deepcopy(_model_pretrained_cfgs[model_name])
    return {}


def register_model(fn):
    """ register models in factory
    """
    # lookup containing module
    mod = sys.modules[fn.__module__]
    module_name_split = fn.__module__.split('.')
    module_name = module_name_split[-1] if len(module_name_split) else ''

    # add model to __all__ in module
    model_name = fn.__name__

    if hasattr(mod, '__all__'):
        mod.__all__.append(model_name)
    else:
        mod.__all__ = [model_name]

    # add entries to registry dict/sets
    _model_entrypoints[model_name] = fn
    _model_to_module[model_name] = module_name
    _module_to_models[module_name].add(model_name)

    # check if model has a pretrained url to allow filtering on this
    has_valid_pretrained = False

    # this will catch all models that have entrypoint matching cfg key, but miss any 
    # aliasing entrypoints or non-matching combos
    if hasattr(mod, 'default_cfgs') and model_name in mod.default_cfgs:

        cfg = mod.default_cfgs[model_name]

        has_valid_pretrained = (
            ('url' in cfg and 'http' in cfg['url']) or
            ('file' in cfg and cfg['file']) or
            ('drive' in cfg and cfg['drive'])
        )

        _model_pretrained_cfgs[model_name] = mod.default_cfgs[model_name]

    # add pretrained
    if has_valid_pretrained:
        _model_has_pretrained.add(model_name)

    return fn


def _natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_.lower())]


def list_models(module='', pretrained=False, name_matches_cfg=False):
    """ list available model names, sorted alphabetically

        pretrained:         bool        include only models with pretrained weights
        name_matches_cfg:   bool        include only models w/ model_name matching 
                                        default_cfg name (excludes some aliases)
    """
    #
    if module:
        models = list(_module_to_models[module])
    else:
        models = _model_entrypoints.keys()

    #
    if pretrained:
        models = _model_has_pretrained.intersection(models)

    #
    if name_matches_cfg:
        models = set(_model_pretrained_cfgs).intersection(models)

    #
    return list(sorted(models, key=_natural_key))
