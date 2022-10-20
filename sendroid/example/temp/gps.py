
from .sensor    import Sensor
from plyer      import gps


class Gps(Sensor):
    GPS_ENABLE  = 'provider-enabled'
    GPS_DISABLE = 'provider-disabled'

    def __init__(
            self,
            update_time: int    = 1000,
            update_dist: float  = 1,
            on_update           = lambda status: None,
            **kwargs
        ):
        """
            Initializes the 'GPS' class instance, starts the GPS updating loop if localization
            service is available and all permissions are granted.
            @param update_time: Time between next GPS updates.
            @param update_dist: Minimum distance from previous update positon to update again.
        """
        self.latitude       = .0
        self.longitude      = .0
        self.speed          = .0
        self.direction      = .0
        self.altitude       = .0
        self.available      = False
        self.update_time    = update_time
        self.update_dist    = update_dist
        self.on_update      = on_update
        super().__init__(
            # buildozer.spec: INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION.
            req_perms   = [
                'ACCESS_FINE_LOCATION',
                'ACCESS_COARSE_LOCATION'
            ],
            **kwargs
        )

    def _on_location(self, **kwargs):
        """
            Callback invoked when location update occurs.
        """
        self.latitude   = kwargs.get('lat',        .0)
        self.longitude  = kwargs.get('lon',        .0)
        self.speed      = kwargs.get('speed',      .0)
        self.direction  = kwargs.get('bearing',    .0)
        self.altitude   = kwargs.get('altitude',   .0)
        self.on_update(status = True)

    def _on_status(self, msg_type, status):
        """
            Callback invoked when state of GPS service changed (e.g. user turned it off).
        """
        if msg_type == Gps.GPS_ENABLE:
            self.available = True
        elif msg_type == Gps.GPS_DISABLE:
            self.available = False
        self.on_update(status = self.available)

    def _on_perms_grant(self, permissions: list, grants: list) -> bool:
        granted = all(grants)
        if granted:
            self.available = True
            # Configure GPS service with callbacks.
            gps.configure(
                on_location = self._on_location,
                on_status   = self._on_status
            )
        return granted

    def _on_enable(self):
        # Start the service with specified update characteristics.
        gps.start(
            minTime     = self.update_time,
            minDistance = self.update_dist
        )
        self.on_enable()

    def _on_disable(self):
        gps.stop()
        self.on_disable()

