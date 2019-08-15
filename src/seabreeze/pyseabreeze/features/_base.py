import functools

from seabreeze.pyseabreeze.exceptions import SeaBreezeError
from seabreeze.pyseabreeze.protocol import ProtocolInterface


class SeaBreezeFeature(object):
    identifier = "base_feature"

    _required_kwargs = ()
    _required_features = ()
    _required_protocol_cls = ProtocolInterface

    def __init__(self, protocol, feature_id, **kwargs):
        """SeaBreezeFeature base class

        Parameters
        ----------
        protocol : seabreeze.pyseabreeze.protocol.ProtocolInterface
        feature_id : int
        """
        if self.identifier == "base_feature":
            raise SeaBreezeError("Don't instantiate SeaBreezeFeature directly. Use derived feature classes.")
        assert set(self._required_kwargs) == set(kwargs)
        # check protocol support
        if not isinstance(protocol, self._required_protocol_cls):
            raise SeaBreezeError("FeatureError: Protocol not supported by feature")
        self.protocol = protocol
        self.feature_id = feature_id

    def __repr__(self):
        return "<{} id={}>".format(self.__class__.__name__, self.feature_id)

    @classmethod
    def get_feature_class_registry(cls):
        # noinspection PyUnresolvedReferences
        return {feature_class.identifier: feature_class for feature_class in SeaBreezeFeature.__subclasses__()}

    @classmethod
    def supports_protocol(cls, protocol):
        return isinstance(protocol, cls._required_protocol_cls)

    @classmethod
    def specialize(cls, **kwargs):
        assert set(kwargs) == set(cls._required_kwargs)
        return functools.partial(cls, **kwargs)