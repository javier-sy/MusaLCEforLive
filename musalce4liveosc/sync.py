from typing import Tuple, Any
from .handler import MusaLCE4LiveOSCHandler, encode_ptr

class SyncHandler(MusaLCE4LiveOSCHandler):

    def init_api(self):
        self.logger.info("SyncHandler loaded")

        def tracks_listener_callback():
            self.logger.info("tracks_listener_callback")
            self.osc_server.send("/musalce4live/tracks", dump_tracks())

        self.tracks_listener_callback = tracks_listener_callback

        def create_midi_listener_callback(track):
            if track in self.midi_listener_callback:
                self.logger.info("using already created midi_listener_callback for track %s" % encode_ptr(track._live_ptr))
                return self.midi_listener_callback[track]
            else:
                self.logger.info("created midi_listener_callback for %s" % encode_ptr(track._live_ptr))
                def callback():
                    self.logger.info("midi_listener_callback")
                    self.osc_server.send("/musalce4live/track/midi_audio", dump_midi(track))

                self.midi_listener_callback[track] = callback
                return callback

        self.midi_listener_callback = {}

        def create_audio_listener_callback(track):
            if track in self.audio_listener_callback:
                self.logger.info("using already created audio_listener_callback for track %s" % encode_ptr(track._live_ptr))
                return self.audio_listener_callback[track]
            else:
                self.logger.info("created audio_listener_callback for %s" % encode_ptr(track._live_ptr))
                def callback():
                    self.logger.info("audio_listener_callback")
                    self.osc_server.send("/musalce4live/track/midi_audio", dump_audio(track))

                self.audio_listener_callback[track] = callback
                return callback

        self.audio_listener_callback = {}

        def create_sub_routing_listener_callback(track):
            if track in self.sub_routing_listener_callback:
                self.logger.info("using already created sub_routing_listener_callback for track %s" % encode_ptr(track._live_ptr))
                return self.sub_routing_listener_callback[track]
            else:
                self.logger.info("created routing_listener_callback for %s" % encode_ptr(track._live_ptr))
                def callback():
                    self.logger.info("sub_routing_listener_callback")
                    self.osc_server.send("/musalce4live/track/routings", dump_routings(track))

                self.sub_routing_listener_callback[track] = callback
                return callback

        self.sub_routing_listener_callback = {}

        def create_name_listener_callback(track):
            if track in self.name_listener_callback:
                self.logger.info("using already created name_listener_callback for track %s" % encode_ptr(track._live_ptr))
                return self.name_listener_callback[track]
            else:
                self.logger.info("created name_listener_callback for %s" % encode_ptr(track._live_ptr))
                def callback():
                    self.logger.info("name_listener_callback")
                    self.osc_server.send("/musalce4live/track/name", dump_name(track))

                self.name_listener_callback[track] = callback
                return callback

        self.name_listener_callback = {}

        def dump_tracks():
            tracks_data = []
            for track in self.song.tracks:
                tracks_data.extend([encode_ptr(track._live_ptr), 
                                    track.name, 
                                    int(track.has_midi_input),
                                    int(track.has_midi_output),
                                    int(track.has_audio_input),
                                    int(track.has_audio_output),
                                    track.current_input_routing, track.current_input_sub_routing,
                                    track.current_output_routing, track.current_output_sub_routing])
                
                set_track_listeners(track)

            return tracks_data

        def dump_midi(track):
            return [encode_ptr(track._live_ptr),
                    int(track.has_midi_input),
                    int(track.has_midi_output)]

        def dump_audio(track):
            return [encode_ptr(track._live_ptr),
                    int(track.has_audio_input),
                    int(track.has_audio_output)]

        def dump_routings(track):
            return [encode_ptr(track._live_ptr),
                    track.current_input_routing, track.current_input_sub_routing,
                    track.current_output_routing, track.current_output_sub_routing]

        def dump_name(track):
            return [encode_ptr(track._live_ptr), track.name]

        def set_listeners():
            self.song.add_tracks_listener(tracks_listener_callback)

            for track in self.song.tracks:
                set_track_listeners(track)

        def set_track_listeners(track):
            if not track in self.midi_listener_callback:
                track.add_has_midi_input_listener(create_midi_listener_callback(track))
                track.add_has_midi_output_listener(create_midi_listener_callback(track))

            if not track in self.audio_listener_callback:
                track.add_has_audio_input_listener(create_audio_listener_callback(track))
                track.add_has_audio_output_listener(create_audio_listener_callback(track))

            if not track in self.sub_routing_listener_callback:
                track.add_current_input_sub_routing_listener(create_sub_routing_listener_callback(track))
                track.add_current_output_sub_routing_listener(create_sub_routing_listener_callback(track))

            if not track in self.name_listener_callback:
                track.add_name_listener(create_name_listener_callback(track))

        def tracks_callback(params: Tuple[Any]):
            self.logger.info("musa4l_tracks_callback")
            return dump_tracks()
        
        set_listeners()

        self.osc_server.add_handler("/musalce4live/tracks", tracks_callback)
        
        tracks_listener_callback()

    def clear_api(self):
        self.song.remove_tracks_listener(self.tracks_listener_callback)
        for track in self.song.tracks:
            track.remove_has_midi_input_listener(self.midi_listener_callback[track])
            track.remove_has_midi_output_listener(self.midi_listener_callback[track])
            track.remove_has_audio_input_listener(self.audio_listener_callback[track])
            track.remove_has_audio_output_listener(self.audio_listener_callback[track])

            track.remove_current_input_sub_routing_listener(self.sub_routing_listener_callback[track])
            track.remove_current_output_sub_routing_listener(self.sub_routing_listener_callback[track])

            track.remove_name_listener(self.name_listener_callback[track])
