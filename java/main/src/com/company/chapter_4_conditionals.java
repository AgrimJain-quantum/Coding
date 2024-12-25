package com.company;
import java.util.Scanner;

public class chapter_4_conditionals {
    public static void main(String[] args) {
//        boolean a = true;
//        boolean b = false;
//        if (a && b){
//            System.out.println("Y");
//        }
//        else{
//            System.out.println("N");
//        }
//
//        boolean a1 = true;
//        boolean b1 = false;
//        if (a1 || b1){
//            System.out.println("y");
//        }
//        else{
//            System.out.println("n");
//        }
//
//        boolean a2 = true;
//        boolean b2 = true;
//        if (a2 || b2){
//            System.out.println("Y");
//        }
//        else{
//            System.out.println("N");
//        }
//        int age;
//        System.out.println("Enter your age - ");
//        Scanner sc = new Scanner(System.in);
//        age = sc.nextInt();
//        if (age>56){
//            System.out.println("You are experinced!");
//        }
//        else if (age>46){
//            System.out.println("You are semi-experinced!");
//        }
//        else if (age>36){
//            System.out.println("You are semi-semi-experinced!");
//        }
//        else{
//            System.out.println("You are not experinced!");
//        }
//        if(age>2){
//            System.out.println("You are not a baby!");
//        }
//        switch(age){
//            case 18:
//                System.out.println("You are going to become an adult!");
//                break;
//            case 21:
//                System.out.println("You are going to get a job!");
//                break;
//            case 31:
//                System.out.println("you die");
//                break;
//            default:
//                System.out.println("Enjoy your rest life");



        //Problem 1
//        int a = 10;
//        if(a == 11){
//            System.out.println("I am 11");
//        }
//        else{
//            System.out.println("I am not 11");
//        }
//        //Problem2
//        byte m1, m2, m3;
//        Scanner sc = new Scanner(System.in);
//        System.out.println("Enter your marks in Physics : ");
//        m1 = sc.nextByte();
//        System.out.println("Enter your marks in chemistry : ");
//        m2 = sc.nextByte();
//        System.out.println("Enter your marks in Mathematics : ");
//        m3 = sc.nextByte();
//        float avg = (m1 + m2 + m3)/3.0f;
//        System.out.println("Your overall percentage is: " + avg);
//        if(avg>=40 && m1>=33 && m2>=33 && m3>=33 ){
//            System.out.println("Congratulations, You have been promoted");
//        }
//        else{
//            System.out.println("Sorry ,  you have not been promoted");
//        }
        //problem 3
//        float tax = 0;
//        float income = 3.3f;
//        if(tax < 2.5){
//            tax = tax + 0;
//        }
//        else if(tax>2.5f && tax<5f){
//            tax = tax + 0.05f * (income - 2.5f);
//        }
//        else if(tax>5f && tax<10.0f){
//            tax = tax + 0.05f * (5.0f - 2.5f);
//            tax = tax + 0.2f * (income - 2.5f);
//        }
//        else if(tax>10f){
//            tax = tax + 0.05f * (5.0f - 2.5f);
//            tax = tax + 0.2f * (10.0f - 5.0f);
//            tax = tax + 0.3f * (income - 2.5f);
//        }
//        System.out.println("The total tax paid by the employee is : " + tax );

//        //Problem 4
////        Scanner sc = new Scanner(System.in);
////        int day = sc.nextInt();
////        switch(day){
////            case 1 -> System.out.println("Monday");
////            case 2 -> System.out.println("Tuesday");
////            case 3 -> System.out.println("Wednesday");
////            case 4 -> System.out.println("Thrusday");
////            case 5 -> System.out.println("Friday");
////            case 6 -> System.out.println("Saturday");
////            case 7 -> System.out.println("Sunday");
//        }
        Scanner sc  = new Scanner(System.in);
        String website = sc.next();
        if (website.endsWith(".org")){
            System.out.println("This is an organizational based website");
        }
        else if (website.endsWith(".com")){
            System.out.println("This is a commercial based website");
        }
        else if (website.endsWith(".in")){
            System.out.println("This is an indian website");
        }
    }
}
