def create_data_directory():
    # creates a new "experiment"
    # creates the Data folder with a default subfolder of 0 and an
    # experiment_count.txt holding the value "0"
    if not os.path.exists("Data/0"):
        os.makedirs("Data/0")
        f = open("Data/experiment_count.txt", "w")
        f.write("0")
        f.close()
    try:
        # increments the experimental counter
        f = open("Data/experiment_count.txt", "r")
        experiment_num = int(f.read()) + 1
        print(experiment_num)
        f.close()
        f = open("Data/experiment_count.txt", "w")
        f.write(str(experiment_num))
        f.close()
    except:
        # defaults to experiment #0 if an error occurs
        print("Error in creating new experiment, defaulting to #0")
        experiment_num = 0
        # try to recreate Data/experiment_count.txt if it is missing
        try:
            f = open("Data/experiment_count.txt", "w")
            f.write("0")
            f.close()
        except:
            print("Error in recreating Data/experiment_count.txt, please resolve issue")
    # creates a subfolder for the experiment if it doesn't exist
    if not os.path.exists(f"Data/{experiment_num}"):
        os.makedirs(f"Data/{experiment_num}")
