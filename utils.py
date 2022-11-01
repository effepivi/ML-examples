import numpy as np
import pandas as pd
import SimpleITK as sitk # Load the medical DICOM file

def getn(df: pd.DataFrame) -> int:
    n = len(df.columns) - 1
    n = df.shape[1] - 1
    return n

def getN(df: pd.DataFrame) -> int:
    N = df.shape[0]
    return N

def applyBiasGain(data, bias, gain):
    return (data + bias) * gain

def loadImage():
    global bias, gain
    fname = "DX000000"

    reader = sitk.ImageFileReader()
    reader.SetFileName(fname)
    sitk_volume = reader.Execute()
    np_image = sitk.GetArrayFromImage(sitk_volume)[0]

    bias = -np.mean(np_image)
    gain = 1.0 / np.std(np_image)

    np_image = applyBiasGain(np_image.astype(np.single), bias, gain)

    window_centre = int(sitk_volume.GetMetaData("0028|1050"))
    window_width = int(sitk_volume.GetMetaData("0028|1051"))

    vmin = applyBiasGain(window_centre - window_width / 2, bias, gain)
    vmax = applyBiasGain(window_centre + window_width / 2, bias, gain)
    
    return np_image, bias, gain, vmin, vmax