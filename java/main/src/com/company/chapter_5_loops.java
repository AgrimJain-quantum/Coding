package com.company;
import java.util.Scanner;


public class chapter_5_loops {
    public static void main(String[] args) {
//        System.out.println("Using loops");
//        int i = 1;
//        while (i<=3){
//            System.out.println(i);
//            i++;
//
//        }
//        System.out.println("Finish running While loop!");
//        while(true){
//            System.out.println("I am an infinite loop");
//        }
//        Scanner sc = new Scanner(System.in);
//        int number = sc.nextInt();
//        while(number>=100 && number<=200){
//            System.out.println(number);
//            number++;
//        }
//        int a = 1;
//        do{
//            System.out.println(a);
//            a++;
////        }while (a<=20);
//        for (int i = 45;i<=100;i++){
//            System.out.println(i);
//        }
// 2n = Even Numbers  = 0, 2, 4, 6,8
// 2n+1 = odd numbers = 1, 3, 5, 7, 9

//        for (int i = 0;i<=5;i++){
//            System.out.println(i);
//            System.out.println("Java is great.");
//            if (i == 2){
//                System.out.println("ENDING THE LOOP");
////                break;
//            }
//        }
//
//        for(int i=0;i<=5;i++){
//            if(i==2){
//                System.out.println("Ending the loop");
//                continue;
//            }
//            System.out.println(i);
//            System.out.println("Java is great");
////        }
        int i = 0;
        do {
            i++;
            if (i == 2) {
                System.out.println("Ending the loop");
                continue;
            }
            System.out.println(i);
            System.out.println("java is great");
        }while(i<5);
        System.out.println("loop ends here");










    }
}
