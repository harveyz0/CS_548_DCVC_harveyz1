#!/bin/sh


#python test_video.py --i_frame_model_name bmshj2018-hyperprior --i_frame_model_path checkpoints/bmshj2018-hyperprior-ms-ssim-3-92dd7878.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-4-4377354e.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-5-c34afc8d.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-6-3a6d8229.pth.tar --test_config dataset_config_rolling.json --cuda true --cuda_device 0 --worker 1 --output_json_result_path DCVC_rolling.json --model_type msssim --recon_bin_path recon_bin_folder_msssim --model_path checkpoints/model_dcvc_quality_0_msssim.pth checkpoints/model_dcvc_quality_1_msssim.pth checkpoints/model_dcvc_quality_2_msssim.pth checkpoints/model_dcvc_quality_3_msssim.pth
#python test_video.py --i_frame_model_name bmshj2018-hyperprior --i_frame_model_path checkpoints/bmshj2018-hyperprior-ms-ssim-3-92dd7878.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-4-4377354e.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-5-c34afc8d.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-6-3a6d8229.pth.tar --test_config dataset_config_high.json --cuda true --cuda_device 0 --worker 1 --output_json_result_path DCVC_high.json --model_type msssim --recon_bin_path recon_bin_folder_msssim --model_path checkpoints/model_dcvc_quality_0_msssim.pth checkpoints/model_dcvc_quality_1_msssim.pth checkpoints/model_dcvc_quality_2_msssim.pth checkpoints/model_dcvc_quality_3_msssim.pth
python test_video.py --i_frame_model_name bmshj2018-hyperprior --i_frame_model_path checkpoints/bmshj2018-hyperprior-ms-ssim-3-92dd7878.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-4-4377354e.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-5-c34afc8d.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-6-3a6d8229.pth.tar --test_config dataset_config_low.json --cuda true --cuda_device 0 --worker 1 --output_json_result_path DCVC_low.json --model_type msssim --recon_bin_path recon_bin_folder_msssim --model_path checkpoints/model_dcvc_quality_0_msssim.pth checkpoints/model_dcvc_quality_1_msssim.pth checkpoints/model_dcvc_quality_2_msssim.pth checkpoints/model_dcvc_quality_3_msssim.pth --write_recon_frame "True"
