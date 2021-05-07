import argparse
import time
from random import randint

parser = argparse.ArgumentParser(description='Finds the longest squence of boxes that fit into one another.')
parser.add_argument("-s","--solution",action="store",dest="solution",default="input.txt",type=str,help="Generate a solution file")
parser.add_argument("-i","--input",action="store_true",dest="input",default=False,help="Generate an input file")
parser.add_argument("-b","--boxes",action="store",dest="boxes",default=10,type=int,help="Set maximum number of boxes to be generated")
parser.add_argument("-m","--maximum",action="store",dest="size",default=50,type=int,help="Set maximum size of boxes to be generated")
results = parser.parse_args()

def fulfill_assumptions(a,b):
    x = 0
    for i in range(0, len(a)):
        if a[i] < b[i]:
            x = a[i]
            a[i] = b[i]
            b[i] = x
    return a, b

def merge(left_a,right_a,left_b,right_b):
    result_a,result_b = [],[]
    while len(left_a)!=0 and len(right_a)!=0:
        if left_a[0]<=right_a[0]:
            result_a.append(left_a[0])
            result_b.append(left_b[0])
            left_a.pop(0)
            left_b.pop(0)
        else:
            result_a.append(right_a[0])
            result_b.append(right_b[0])
            right_a.pop(0)
            right_b.pop(0)
    while len(left_a)!=0:
        result_a.append(left_a[0])
        result_b.append(left_b[0])
        left_a.pop(0)
        left_b.pop(0)
    while len(right_a)!=0:
        result_a.append(right_a[0])
        result_b.append(right_b[0])
        right_a.pop(0)
        right_b.pop(0)
    return result_a,result_b

def merge_sort(a,b):
    if len(a)<=1: return a,b
    half_a=int(len(a)/2)
    left_a,left_b = merge_sort(a[:half_a],b[:half_a])
    right_a,right_b = merge_sort(a[half_a:],b[half_a:])
    return merge(left_a,right_a,left_b,right_b)
    
def lis(a,b):
    n = len(a)
    d,q = [1]*n,[-1]*n
    for i in range(1,n):
        for j in range(0,i):
            if a[j]<a[i] and d[i]<(d[j]+1): d[i],q[i] = d[j]+1,j
    res,pos = d[0],0
    for i in range(1,n):
        if d[i]>res: res,pos = d[i],i
    p = []
    k = []
    while pos!=-1:
        p.append(a[pos])
        k.append(b[pos])
        pos = q[pos]
    p = list(reversed(p))
    k = list(reversed(k))
    return k, p, res

def create_array(size=10,max=50):
    return [randint(0,max) for _ in range(size)]

def generate_input(boxes,size):
    print("Generating boxes...")
    num_boxes,max_size = int(boxes),int(size)
    w,l = create_array(num_boxes,max=max_size),create_array(num_boxes,max=max_size)
    f = open("input.txt","w+")
    f.write(str(num_boxes)+"\n")
    for i in range(num_boxes):
        if i==num_boxes-1:
            f.write(str(l[i])+' '+str(w[i]))
        else:
            f.write(str(l[i])+' '+str(w[i])+'\n')
    f.close()
    print(str(num_boxes)+" boxes generated successfully with maximum size set to "+str(max_size))

def generate_solution(path):
    start_time = time.time()
    print("Generating solution...")
    l,w = [],[]
    with open(path) as f:
        num_boxes = int(f.readline())
        for line in f:
            l.append(int(line.split(' ')[0]))
            w.append(int(line.split(' ')[1].split('\n')[0]))
    if len(l) == 0:
        print("There are no solutions if no boxes exit")
        return
    initial_l = l
    l,w = fulfill_assumptions(l,w)
    l,w = merge_sort(l,w)
    k,p,res = lis(w,l)
    output = ""
    for i in range(len(k)):
        if i > 0 and int(k[i]) == int(k[i-1]):
            res-=1
        elif int(k[i]) == 0 or int(p[i]) == 0:
            res-=1
        else:
            output+="box "+str(initial_l.index(k[i]))+" with ("+str(k[i])+","+str(p[i])+") < \n"
    f = open("output.txt","w+")
    f.write("From the "+str(num_boxes)+" input boxes:\nThe maximum number of boxes that can be stacked inside one another is "+str(res)+"\r\n")
    f.write(output[:-2])
    f.close()
    print("Solution generated successfully in %s seconds"%(time.time()-start_time))

def main(solution,input,boxes,size):
    if input:
        generate_input(boxes,size)
    if solution is not None:
        generate_solution(solution)

if __name__=='__main__':
    main(results.solution,results.input,results.boxes,results.size)