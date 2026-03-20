#include<iostream>
using namespace std;


template <typename T>
struct node
{
    T data;
    node<T>* next;
};


template <class T>
class queue
{
private:
    node<T>* head;

public:
queue():head(nullptr){}

void enqueue(T value){

if(head!=nullptr)
{
    node<T>*temp = head;
    while(temp->next!=nullptr)
    {
        temp = temp->next;
    }
    temp->next = new node<T>;
    temp->next->data = value; 
    temp->next->next = nullptr;
}
else
{
    head = new node<T>;
    head->data = value;
    head->next = nullptr;
}

cout<<"new item successfully added"<<endl;
node<T>* display = head;
while(display!=nullptr)
{
    cout<<display->data<<"<----";
    display = display->next;
}
cout<<endl;
}



void dequeue()
{
if(head!=nullptr)
{


    node<T>* temp = head;
    head = temp->next;
    temp->next = nullptr;
    delete temp;
}
else
{
    cout<<"already deleted !"<<endl;
    return;
}


cout<<"successfully dequeued first item"<<endl;
node<T>* display = head;
while(display!=nullptr)
{
    cout<<display->data<<"<----";
    display = display->next;
}
cout<<endl;


}



void get_Nth_element_from_front(T val)
{

    node<T>* temp = head;
    int counter = 0;
    while(temp!=nullptr)
    {
        if(counter==val)
        {
            cout<<"Getting Nth element "<<endl;
            cout<<temp->data<<endl;
            break;}
        counter++;
        temp = temp->next;
    }
    

}


void get_Nth_element_removed(T val)
{
    node<T>* prev = nullptr;
    node<T>* temp = head;
    int counter = 0;
    while(temp!=nullptr)
    {

        if(counter==val)
        {
            
            
        }
        counter++;
        prev = temp;
        temp = temp->next;

    }
    
}












void isEmpty()
{
if(head!=nullptr)
cout<<"Not empty"<<endl;
else
cout<<"Empty"<<endl;
}


void first()
{
    if(head!=nullptr)
    cout<<head->data<<endl;
    else
    cout<<"No queue exist"<<endl;
}


void size()
{
    int counter = 0;
     node<T>*temp = head;
    while(temp!=nullptr)
    {
        counter++;
        temp = temp->next;
    }

    if(counter!=0)
    cout<<"the size is "<<counter<<endl;
    else
    cout<<"The list is empty"<<endl;
}


void display()
{

    node<T>*temp = head;
    while(temp!=nullptr)
    {
        cout<<temp->data<<"<---";
        temp = temp->next;
    }

}


};







int main()
{
    queue<int> q;

    cout << "Queue initially:\n";
    q.isEmpty();

    cout << "\nEnqueue operations:\n";
    q.enqueue(10);
    q.enqueue(20);
    q.enqueue(30);
    q.enqueue(40);

    cout << "\nCheck size:\n";
    q.size();

    cout << "\nCheck first element:\n";
    q.first();

    cout << "\nDequeue operations:\n";
    q.dequeue();
    q.dequeue();

    cout << "\nCurrent queue:\n";
    q.display();

    cout << "\nFinal size:\n";
    q.size();

    cout << "\nCheck if empty:\n";
    q.isEmpty();

    return 0;
}



 