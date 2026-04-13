from utilities import bitrate_recovery, environmental_fix, denoising_engine, spatial_refinement

class ForensicVSR_Pipeline2:
    def __init__(self, frame):
        self.original_frame = frame
        self.working_frame = frame.copy()

    def step_1_bitrate(self, apply=True):
        if apply:
            self.working_frame = bitrate_recovery.recover_bitrate_artifacts(self.working_frame)
        return self.working_frame

    def step_2_environment(self, relight=True, dehaze=True):
        if relight:
            self.working_frame = environmental_fix.apply_retinex_relighting(self.working_frame)
        if dehaze:
            self.working_frame = environmental_fix.apply_atmospheric_veil(self.working_frame)
        return self.working_frame

    def step_3_denoise(self, apply=True):
        if apply:
            self.working_frame = denoising_engine.apply_denoising(self.working_frame)
        return self.working_frame

    def step_4_upscale(self, factor=2):
        self.working_frame = spatial_refinement.upscale_video_frame(self.working_frame, factor)
        return self.working_frame

    def step_5_sharpen(self, apply=True):
        if apply:
            self.working_frame = spatial_refinement.apply_sharpening(self.working_frame)
        return self.working_frame

    def get_final_result(self):
        return self.working_frame