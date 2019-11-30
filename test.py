def twodmodel():
    with open("/opt/lampp/htdocs/hack/tmp.txt",'r') as f:
        line = f.readline()
        line = line[1:]
        line = line[:-1]
        list_pts = line.split(',')
        points = list()
        for pt in list_pts:
            pt= pt.replace('[','')
            pt = pt.replace(']','')
            points.append(pt)

    ptuple = list()
    k = 0
    for i in range(0,4):
        ptuple.append((points[k],points[k+1]))
        k+= 2
    
    return ptuple
twodmodel()

