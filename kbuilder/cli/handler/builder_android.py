"""Android build handler."""

from kbuilder.cli.handler.builder_linux import LinuxBuilderHandler
from kbuilder.cli.interface.builder_android import IAndroidBuilder

from unipath.path import Path


class AndroidBuilderHandler(LinuxBuilderHandler):
    class Meta:
        interface = IAndroidBuilder
        label = 'android_builder_handler'
        description = 'Handler for building android targets'

    def __init__(self, **kw_args):
        super().__init__(**kw_args)
        self.ota_source_dir = None
        self.toolchain = None

    def _setup(self, app):
        super()._setup(app)
        name = self.kernel.name
        self.ota_source_dir = Path(app.config.get(name, 'ota_dir')).expand_user()
        self.toolchain = self.app.db.retrieve('default_toolchain')

    def build_ota_package(self):
        self.build_kbuild_image()
        kernel = self.kernel
        ota = kernel.make_ota_package(kbuild_image_dir='boot',
                                      source_dir=self.ota_source_dir,
                                      output_dir=self.export_path)
        self.app.log.info('created ' + ota)

    def build_kbuild_image(self) -> None:
        """Build a kbuild image with the default toolchain."""
        self.toolchain.set_as_active()
        self.kernel.extra_version = self.toolchain.name

        info = 'Compiling {0} with {1}'.format(self.kernel.release_version,
                                               self.toolchain)
        self.log.info(info)

        self.kernel.arch_clean()
        self.kernel.build_kbuild_image(self.build_log_dir)
        self.log.info('{0.kbuild_image} created'.format(self.kernel))

    def build_boot_image(self):
        pass
