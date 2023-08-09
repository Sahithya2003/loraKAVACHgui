import time
import numpy as np
from gnuradio import blocks
from gnuradio import gr
from gnuradio import analog
from gnuradio.filter import firdes
from grlora import lora

class lora_simulator(gr.top_block):
    def _init_(self):
        gr.top_block._init_(self, "LoRa Simulator")

        ##################################################
        # Parameters
        ##################################################
        samp_rate = 1e6  # Sample rate
        freq_initial = 868e6  # Initial frequency
        freq_indian_standard = 865e6  # Indian standard frequency for LoRa
        freq_another = 869e6  # Another frequency for LoRa after 30 seconds

        ##################################################
        # Blocks
        ##################################################
        self.source_initial = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_initial, 1, 0)
        self.source_indian_standard = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_indian_standard, 1, 0)
        self.source_another = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_another, 1, 0)
        
        self.lora_mod = lora.lora_mod()  # Use lora module to modulate the source

        self.file_sink = blocks.file_sink(gr.sizeof_gr_complex, 'lora_capture.cfile', False)
        self.file_sink.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect(self.source_initial, self.lora_mod, self.file_sink)

        # Simulate frequency change after 10 seconds
        time.sleep(10)
        self.disconnect(self.source_initial, self.lora_mod, self.file_sink)
        self.connect(self.source_indian_standard, self.lora_mod, self.file_sink)
        
        # Simulate another frequency change after 30 seconds
        time.sleep(30)
        self.disconnect(self.source_indian_standard, self.lora_mod, self.file_sink)
        self.connect(self.source_another, self.lora_mod, self.file_sink)

        # Run the simulation for 1 minute
        time.sleep(20)

        # Stop the flowgraph
        self.stop()
        self.wait()

if __name__ == '_main_':
    tb = lora_simulator()
    tb.run()