from live_advance import LiveAdvance
import threading
from datetime import datetime
import time

class EEGInterface:
    def __init__(self, your_app_client_id, your_app_client_secret, your_app_license, record_export_folder,
                 record_export_format, record_export_version, headset_id, profile_name):
        self.headset_id = headset_id
        self.profile_name = profile_name

        self.record_export_folder = record_export_folder
        self.record_export_format = record_export_format
        self.record_export_version = record_export_version

        #  initialize markers
        self.control_marker = 0
        self.game_marker = 0
        self.record = False

        # Init live advance
        self.liveAdvance = LiveAdvance(your_app_client_id, your_app_client_secret, license=your_app_license)
        threadName = "EEGThread:-{:%Y%m%d%H%M%S}".format(datetime.utcnow())
        self.eeg_thread = threading.Thread(target=self.beginStream, name=threadName)
        self.eeg_thread.daemon = True
        self.eeg_thread.start()

    def beginStream(self):
        self.liveAdvance.start(self.profile_name, self.headset_id)

    # opens and runs session
    def streamLineData(self):
        # collect each line of stdout from live_advance.py
        '''data: dictionary
             the format such as {'action': 'neutral', 'power': 0.0, 'time': 1590736942.8479}'''
        output = self.liveAdvance.data
        if output:
            # determines / executes action
            return output['action'], output['power']

    def createRecording(self):
        record_path = f"EEG-Game_{self.profile_name}_{self.headset_id}"
        record_description = "A test of the eeg game recording system"
        self.liveAdvance.create_record(record_path, description=record_description)
        self.record = True


    def endRecording(self):
        self.liveAdvance.record_export_folder = self.record_export_folder
        self.liveAdvance.record_export_format = self.record_export_format
        self.liveAdvance.record_export_version = self.record_export_version

        if self.liveAdvance.record_export_format == 'EDF':
            self.liveAdvance.record_export_data_types = ['EEG']
        elif self.liveAdvance.record_export_format == 'CSV' and self.liveAdvance.record_export_version == 'V1':
            self.liveAdvance.record_export_data_types = ['EEG']
        elif self.liveAdvance.record_export_format == 'CSV' and self.liveAdvance.record_export_version == 'V2':
            self.liveAdvance.record_export_data_types = ['EEG', 'MOTION', 'PM', 'BP']
        #  (folder, stream_types, format, record_ids, version, **kwargs)
        self.record = False
        self.liveAdvance.stop_record()

    def add_control_marker(self, direction):
        if self.record is True:
            marker_time = time.time() * 1000

            self.control_marker += 1

            # marker_label
            label = f"Control:_{self.headset_id}_{str(self.control_marker)}"

            self.liveAdvance.inject_marker(marker_time, direction, label, port='EEG-Game')

    def add_game_marker(self):
        if self.record is True:
            marker_time = time.time() * 1000

            self.game_marker += 1

            # marker_label
            label = f"Game:_{str(self.game_marker)}"

            self.liveAdvance.inject_marker(marker_time, 1, label, port='EEG-Game')

    def end_control_marker(self):
        if self.record is True:
            if self.liveAdvance.last_marker_id is not None:
                marker_time = time.time() * 1000
                self.liveAdvance.update_marker(self.liveAdvance.last_marker_id, marker_time)
                self.liveAdvance.last_marker_id = None
