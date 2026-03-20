#include <iostream>
using namespace std;
/*
Question:
You have to model a garage system. The garage has a list of cars, Parking slots, time, and money.
You get charged as per in/out of garage.
You are owner of slot.
*/


/*
Solution:
- identify classes
- identify attributes
- identify relationships (abstract, composition, aggregation)
- identify methods
- identify inheritance (if exists)
*/


/*
Types of relationships:
-Composition: 'X' class has a 'Y' class in it. for example, a car has an engine, garage has a car etc; 
*/


/*
class diagram:
|garage|<>-----|slot|<>------|time|
|slot|<>------|car|
*/


class Time{
    private:
    int hour;
    int minute;
    int second;
};


class car{
    private:
    string model;
    string registationNumber;
    string color;
    string number;
    string owner;
};

//this is the composition of time and car.
class slot
{
    private:
    int slotNumber;
    car car;
    Time time;
    double price; //some slots are more expensive than others.

};

// this is the composition of slot.
class garage{

    private:
    int garageNumber;
    slot slot;

};





