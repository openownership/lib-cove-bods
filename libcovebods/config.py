from libcove.config import LIB_COVE_CONFIG_DEFAULT, LibCoveConfig

LIB_COVE_BODS_CONFIG_DEFAULT = LIB_COVE_CONFIG_DEFAULT.copy()

LIB_COVE_BODS_CONFIG_DEFAULT.update({

})


class LibCoveBODSConfig(LibCoveConfig):
    def __init__(self, config=LIB_COVE_BODS_CONFIG_DEFAULT):
        self.config = config
