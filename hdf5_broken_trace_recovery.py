import h5py
import os
import shutil

if __name__ == "__main__":
    # the current working directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # file name of the broken HDF5 or MAT file
    corrupted_file_name = "source.mat"
    corrupted_file_path = os.path.join(script_dir, corrupted_file_name)

    # recovered file name
    recovered_file_name = "source_rec.mat"
    recovered_file_path = os.path.join(script_dir, recovered_file_name)

    # create a copy of the corrupted file
    try:
        shutil.copyfile(corrupted_file_path, recovered_file_path)
        print(f"HDF5 file '{corrupted_file_name}' copied to '{recovered_file_name}' successfully.")
    except FileNotFoundError:
        print(f"Error: Source file '{corrupted_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # open file for read and write
    with h5py.File(recovered_file_path, 'r+') as f:
        # here is the corrupted dataset field
        data_dset = f['Channel_2/Data']
        # get the info on the chunks
        dset_chunk_info = data_dset.chunks
        # extract the chunk size
        dset_chunk_size = dset_chunk_info[1]
        # total number of the chunks
        total_chunks = data_dset.size // dset_chunk_size

        # create a set of corrupted chunk indices
        exclude_set = set()

        # fill in the indices set
        for k in range(0,total_chunks):
            try:   
                # read the data in chunks by precisely addressing indices 
                data_dset[0, dset_chunk_size*k : dset_chunk_size*(k+1)]
            except:
                exclude_set.add(k)

        # list of replacement dummy values to store instead of broken chunks
        lost_vals_replacement = [999999 for d in range(0,dset_chunk_size)]

        # list of the output values 
        out_vals = list()
        
        # fill in the list
        for k in range(0,total_chunks):
            if k not in exclude_set:
                out_vals.extend(data_dset[0, dset_chunk_size*k : dset_chunk_size*(k+1)])
            else:
                print('here we go!')
                out_vals.extend(lost_vals_replacement)
        
        # rewrite the corrupted data
        data_dset[...] = out_vals

        # print the indices of chunks that were corrupted
        print(exclude_set) 

        # close file
        f.close() 
