from typing import Any, Dict, List, Mapping

__all__ = ['Namespace', 'namespacify']

#-- Namespaces ----------------------------------------------------------------

class Namespace(Dict[str, Any]):
    '''
    A `dict` that supports accessing items as attributes
    '''
    def __dir__(self) -> List[str]:
        return list(set([*dict.__dir__(self), *dict.__iter__(self)]))

    def __getattr__(self, key: str) -> Any:
        return dict.__getitem__(self, key)

    def __setattr__(self, key: str, val: object) -> None:
        dict.__setitem__(self, key, val)

    def __delattr__(self, key: str) -> None:
        dict.__delitem__(self, key)

    @property
    def __dict__(self) -> dict: # type: ignore
        return self
    
    def __repr__(self):
        import pprint
        return f"{self.__class__}\n{pprint.pformat(_to_dict(self))}"


def namespacify(obj: object) -> object:
    '''
    Recursively convert mappings (item access only) and ad-hoc namespaces
    (attribute access only) to `Namespace`s (both item and element access).
    '''
    if isinstance(obj, (type(None), bool, int, float, str)):
        return obj
    elif isinstance(obj, list):
        return [namespacify(v) for v in obj]
    elif isinstance(obj, Mapping):
        return Namespace({k: namespacify(obj[k]) for k in obj})
    else:
        return namespacify(vars(obj))


def _to_dict(obj: object) -> dict:
    '''
    Recursively convert `Namespace`s to mappings. Inverse operation to
    namespacify.
    '''
    if isinstance(obj, Namespace):
        return dict( (k, _to_dict(v)) for k,v in obj.__dict__.items() )
    elif isinstance(obj, (list, tuple)):
        return type(obj)( _to_dict(v) for v in obj )
    else:
        return obj