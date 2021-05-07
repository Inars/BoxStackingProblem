import time
import tkinter as tk
import matplotlib.pyplot as plt
from random import randint

class Lotfi(tk.Entry):
    def __init__(self, master=None,**kwargs):
        self.var = tk.StringVar()
        tk.Entry.__init__(self,master,textvariable=self.var,**kwargs)
        self.old_value = ''
        self.var.trace('w',self.check)
        self.get,self.set = self.var.get,self.var.set

    def check(self,*args):
        if self.get().isdigit(): 
            self.old_value = self.get()
        else:
            self.set(self.old_value)

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

def generate_boxes(num_boxes=10,max_size=50):
    output_1.insert("end","Generating boxes...")
    num_boxes,max_size = int(input_1.get()),int(input_2.get())
    w,l = create_array(num_boxes,max=max_size),create_array(num_boxes,max=max_size)
    f = open("input.txt","w+")
    f.write(str(num_boxes)+"\n")
    for i in range(num_boxes):
        if i==num_boxes-1:
            f.write(str(l[i])+' '+str(w[i]))
        else:
            f.write(str(l[i])+' '+str(w[i])+'\n')
    f.close()
    output_1.insert("end",str(num_boxes)+" boxes generated successfully with maximum size set to "+str(max_size))

def generate_solution():
    start_time = time.time()
    output_1.insert("end","Generating solution...")
    l,w = [],[]
    with open('input.txt') as f:
        num_boxes = int(f.readline())
        for line in f:
            l.append(int(line.split(' ')[0]))
            w.append(int(line.split(' ')[1].split('\n')[0]))
    if len(l) == 0:
        output_1.insert("end","There are no solutions if no boxes exit")
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
    output_1.insert("end","Solution generated successfully in %s seconds"%(time.time()-start_time))

def plot_time_complexity():
    output_1.insert("end","Calculating time complexity, this may take a few minutes...")
    button_3.config(state=tk.DISABLED)
    runtimes,boxes = [],[]
    for i in range(100,10100,100):
        start_time = time.time()
        w,l = create_array(size=i),create_array(size=i)
        l,w = fulfill_assumptions(l,w)
        l,w = merge_sort(l,w)
        p,res = lis(w)
        runtimes.append(time.time()-start_time)
        boxes.append(i)
    plt.plot(boxes,runtimes)
    plt.ylabel("runtime")
    plt.xlabel("boxes count")
    plt.show()
    button_3.config(state=tk.NORMAL)
    output_1.insert("end","Time complexity plotted successfully")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Boxes")
    root.iconbitmap("box.ico")
    root.resizable(False, False)
    
    output_1 = tk.Listbox(root)
    output_1.grid(row=7,column=0,columnspan=2,pady=5,padx=5,sticky=tk.W+tk.E)
    output_1.insert("end","Initializing...")
    
    label_1 = tk.Label(root,text="Wlecome to the Boxes application!",fg="blue",font="bold")
    label_1.grid(row=0,column=0,columnspan=2,padx=80,pady=10,sticky=tk.W+tk.E)
    
    label_2 = tk.Label(root,text="Number of Boxes to generate",padx=5,anchor=tk.W)
    label_2.grid(row=1,column=0,sticky=tk.W+tk.E)
    input_1 = Lotfi(root,width=10)
    input_1.insert(0, "10")
    input_1.grid(row=1,column=1)
    
    label_3 = tk.Label(root,text="Maximum size of the boxes",padx=5,anchor=tk.W)
    label_3.grid(row=2,column=0,sticky=tk.W+tk.E)
    input_2 = Lotfi(root,width=10)
    input_2.insert(0,"50")
    input_2.grid(row=2,column=1,pady=10)
    
    label_4 = tk.Label(root,text="Generate boxes file",padx=5,anchor=tk.W)
    label_4.grid(row=3, column=0,sticky=tk.W+tk.E)
    button_1 = tk.Button(
        root,
        text="Generate Boxes",
        padx=50,
        command=lambda:generate_boxes(num_boxes=input_1.get(),max_size=input_2.get()))
    button_1.grid(row=3,column=1)
    
    label_5 = tk.Label(root,text="Generate solution file",padx=5,anchor=tk.W)
    label_5.grid(row=4,column=0,sticky=tk.W+tk.E)
    button_2 = tk.Button(
        root,
        text="Generate Solution",
        padx=43.5,
        command=generate_solution)
    button_2.grid(row=4,column=1,pady=10)
    
    button_3 = tk.Button(
        root,
        text="Plot Time Complexity",
        padx=10,
        command=plot_time_complexity)
    button_3.grid(row=5,column=0,columnspan=2)
    
    label_6 = tk.Label(root, text="Log",anchor=tk.W)
    label_6.grid(row=6,column=0,padx=5,sticky=tk.W+tk.E)
    
    output_1.insert("end","Initialized")
    
    root.mainloop()