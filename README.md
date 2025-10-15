# hdf5-scope-recovery
Data recovery from a corrupted oscilloscope Matlab/HDF5 file.

Sometimes, it happens that the time traces (or waveforms) that are exported from an oscilloscope (e.g., from Keysight brand) get corrupted, and you cannot import them to Python or Matlab.
In Python, one get 'Can't read data (inflate() failed)' error, Matlab will not load it, Julia gets 'HDF5.API.H5Error("Error reading dataset...")', etc.
While being rare, such a situation can create a lot of frustration and grey hair.

Fortunately, the HDF5 format that lies in the heart of .h5 and .mat files exported by the scope, uses chunks to write the data. And while the corruption makes reading a dataset from a field as a whole impossible, it is still possible to read the dataset in chunks skipping the corrupted ones, and recover at least some data.

This simple script does exactly that. First, it finds the corrupted chunks. Then it overwrites the field with the values where the corrupted ones are replaced with some dummy values.

I really hope that this little tool will help to save some nerve cells.
