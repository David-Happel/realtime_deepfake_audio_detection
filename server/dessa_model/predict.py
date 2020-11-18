import os
from utils import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

# Load the pretrained model
# pretrained_model_name = 'saved_model_80_8_32_0.1_1_50_0.0001_1000_16_True.h5'
pretrained_model_name = 'saved_model_240_8_32_0.05_1_50_0_0.0001_100_156_2_True_True_fitted_objects.h5'

discriminator = Discriminator_Model(load_pretrained=True, saved_model_name=pretrained_model_name)
discriminator.model._make_predict_function()


def predict(dirpath, filename):

    # Directory from which we read the data
    # data_dir = "../data/inference_data/"
    mode = "unlabeled"  # real, fake, or unlabeled

    # Convert files to flac
    # convert_to_flac(os.path.join(data_dir,mode))

    # preprocess the files
    # processed_data = preprocess_from_ray_parallel_inference(data_dir, mode, use_parallel=False)
    processed_data = [process_audio_files_inference(filename, dirpath, mode)]

    # Visualize the preprocessed data
    # plot_spectrogram(processed_data[0], path='visualize_inference_spectrogram.png')

    return discriminator.predict_labels(processed_data, raw_prob=True, batch_size=20)[0][0]


if __name__ == '__main__':
    print(predict("audio/", "1_file.wav"))
