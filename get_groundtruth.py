import get_data as gd

def ReadMannualDataLine(filename):

        with open(filename, 'rU') as f:
                truth  = [l.split('\t') for l in f.read().splitlines()]
        #return description for this ground truth
        description = [t[4] for t in truth]
        return description 


def ReadPhoenixDataLine(filename):

	    names=[line.strip() for line in open(filename)]


	    #label violation event as 1, other aas 0
	    violation = []
	    for items in names:
	    	items = items.split('\t')
	    	if(items[16] < 0.0):
	    		if(items[17] != 'nan'):
	    			event = (items[17], 1)
	    			violation.append(event)
	    	else:
	    		if(items[17] != 'nan'):
	    			event = (items[17], 0)
	    			violation.append(event)

	    return violation




if __name__ == "__main__":
        data_dir = gd.GetDataDirList()

        description = ReadMannualDataLine(data_dir[0] + 'Yemen_Events_Manual.txt')
        out = open("description.txt", "w")
        for item in description:
                out.write(item +'\n')

        out.close()

        
        phoenix = ReadPhoenixDataLine(data_dir[0] + 'yemen_phoenix.txt')

        out = open("phoenix_event.txt", "w")

        for item in phoenix:
                out.write(str(item[0])+'\t'+str(item[1]) +'\n')
        
	out.close()
