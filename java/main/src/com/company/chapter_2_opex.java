package com.company;
import java.util.Scanner;

public class chapter_2_opex {
    public static void main(String[] args) {
        //Problem 1
        float a = 7/4.0f * 9/2.0f;
        System.out.println(a);
        //Problem 2
        char grade = 'B';
        grade = (char)(grade + 8);
        System.out.println(grade);
        grade = (char)(grade - 8);
        System.out.println(grade);
        //Problem 3
        Scanner sc = new Scanner(System.in);
        int b = sc.nextInt();
        System.out.println(b>8);


    }
}
