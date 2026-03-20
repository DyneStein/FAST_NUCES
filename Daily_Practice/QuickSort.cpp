#include<iostream>
using namespace std;

void swap(int& a, int& b)
{
    int temp = a;
    a = b;
    b = temp;
}

void quickSort(int arr[], int i , int j)
{

int low = i;
int high = j;

if(i<j)
{

    //partitioning starts here.
    int pivot = arr[i];
    while(low<high)
    {

        while(arr[low]<pivot || arr[low]==pivot)low++;
        while(arr[high]>pivot)high--;
        if(low>high) break; // very important conditon.
        swap(arr[low],arr[high]);
        low++; high--;
    }

    swap(arr[i],arr[high]); // partitioning done here.

    quickSort(arr, i, high);
    quickSort(arr, high+1,j);
}


}


int main()
{
    int arr[] = {45,50,6000,30,22,11,74,88,99};
    quickSort(arr,0,8);
    for(int i = 0;i<9;i++)
    {
        cout<<arr[i]<<" ";
    }



    return 0;
}