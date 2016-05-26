import get_data as gd

def ReadDataLine(filename):

        with open(filename, 'rU') as f:
                truth  = [l.split('\t') for l in f.read().splitlines()]
        return truth


if __name__ == "__main__":
        data_dir = gd.GetDataDirList()
        truth = ReadDataLine(data_dir[0] + 'Yemen_Events_Manual.txt')	
	description = [t[4] for t in truth]
	out = open("description.txt", "w")

        for item in description:
                out.write(str(item)+'\n')

        out.close()
        #print(truth)
