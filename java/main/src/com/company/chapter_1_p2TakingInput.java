package com.company;
import java.util.Scanner;

public class chapter_1_p2TakingInput {
    public static void main(String[] args) {
        Scanner a = new Scanner(System.in);
        System.out.println("enter a number v: ");
        float v = a.nextFloat();
        System.out.println("enter a number u: ");
        float u = a.nextFloat();
        System.out.println("enter a number b: ");
        float b = a.nextFloat();
        System.out.println("enter a number s: ");
        float s = a.nextFloat();
        float result;
        result = ((v*v) - (u*u))/(2*b*s);
        System.out.println(result);
    }
}



