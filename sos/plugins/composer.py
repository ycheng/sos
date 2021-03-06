from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin


class Composer(Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin):
    """Lorax Composer
    """

    plugin_name = 'composer'
    profiles = ('sysmgmt', 'virt', )

    packages = ('composer-cli',)

    def _get_blueprints(self):
        blueprints = []
        bp_file = self.get_cmd_output_now("composer-cli blueprints list")
        if bp_file:
            with open(bp_file, "r") as bps:
                for line in bps.read().splitlines():
                    blueprints.append(line)
        return blueprints

    def setup(self):
        self.add_copy_spec([
            "/etc/lorax/composer.conf",
            "/var/log/lorax-composer/composer.log"
            "/var/log/lorax-composer/dnf.log"
            "/var/log/lorax-composer/program.log"
            "/var/log/lorax-composer/server.log"
        ])
        blueprints = self._get_blueprints()
        for blueprint in blueprints:
            self.add_cmd_output("composer-cli blueprints show %s" % blueprint)

        self.add_cmd_output("composer-cli sources list")

# vim: set et ts=4 sw=4 :
