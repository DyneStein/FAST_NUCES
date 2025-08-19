#include<iostream>
using namespace std;

struct node
{
    int data;
    node* next;
};


class List_of_Nodes
{
    private:
    int value;
    node* head = nullptr;

    public:

    node* getHead()
    {
        return head;
    }

    void addNodes(int val)
    {
        if(!(head))
        {
            head = new node;
            head->data = val;
            cout<<"Head node created !"<<endl;
        }
        else
        {
            node* temp = head;
            while(temp->next)
            {
                temp = temp->next;
            }
            temp->next = new node;
            temp->next->data = val;
            cout<<"node successfully added !"<<endl;
        }
    }


    void close_chain()
    {
            node* temp = head;
            while(temp->next)
            {
                temp = temp->next;
            }
            temp->next = head;
            cout<<"Cycle completed successfully !"<<endl;
    }


    void checkCycle(node* head)
    {
            node* temp = head;
            while(temp->next)
            {
                temp = temp->next;
                if((temp->next) == head)
                {cout<<"Cycle exists ! "<<endl; break;}
                else if(!(temp->next))
                cout<<"Cycle does not exist !"<<endl;
            }
    }

    void deleteNode(int val)
    {
        node* Prev = head;
        node* Next = head->next;

        while(Next->next)
        {
            if(Next->data == val)
            {
                node* temp = Next->next;
                Prev->next = temp;
                cout<<"Node successfully deleted !"<<endl;
                break;
            }
            
            Next = Next->next;
            Prev = Prev->next;
        }

    }


    void displayNodes()
    {
        node* temp = head;
        int counter = 1;
        while(temp->next)
        {
            cout<<"Node "<<counter<<" value : "<<temp->data<<endl;
            temp = temp->next;
            counter++;
        }
        cout<<"Node "<<counter<<" value : "<<temp->data<<endl;
    }


    void deallocate()
    {

        if(!(head->next))
        delete head;
        else
        {

        node* temp = head->next;
        while(temp->next){
        temp = head->next;
        delete head;
        head = temp;
        }
        delete temp;

    }

    }

};


int main()
{

    cout<<"Welcome"<<endl;
    List_of_Nodes List;

    cout<<"Choose from the following options "<<endl;
    while(true)
    {
        cout<<"Select a number from the following "<<endl;
        cout<<"1 - Add a Node\n2- Display Nodes\n3- Delete a specific node\n4-Make cycle\n5-Check Cycle\n6-Exit"<<endl;
        int input;
        cin>>input;
        if(input==1)
        {
            int x;
            cout<<"Enter the value for node :";
            cin>>x;
            List.addNodes(x);
        }
        else if(input == 2)
        {
            List.displayNodes();
        }
        else if(input == 3)
        {
            int x;
            cout<<"Enter the node value to be deleted :";
            cin>>x;
            List.deleteNode(x);
        }
        else if(input ==4)
        {
            List.close_chain();
        }
        else if(input ==5)
        {
            List.checkCycle(List.getHead());
        }
        else if(input ==6)
        {
            List.deallocate();
            return 0;
        }


    }




    return 0;
}