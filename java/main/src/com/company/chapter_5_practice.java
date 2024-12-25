package com.company;

public class chapter_5_practice {
    public static void main(String[] args) {
        //problem 1
//        int rows = 4;
//        for(int i = rows; i > 0; i--){
//            for(int j = 0; j < i; j++){
//                System.out.print("*");
//            }
//            System.out.println();
//        }
//        //problem 2
//        int sum = 0;
//        int n = 3;
//        for(int i = 0;i<n; i++ ){
//            sum = sum + (2*i);
//        }
//        System.out.print("Sum of even numbers is: ");
//        System.out.println(sum);
        //problem 3
//        int n = 5;
//        //[for(int i=0; i<10; i++) - goes from 0 to 9
//        for(int i = 0; i<=10; i++ ){
//            System.out.printf("%d x %d = %d\n" , n, i, n*i);
//        }
        //problem 4
//        int x = 10;
//        //[for(int i=0; i<10; i++) - goes from 0 to 9
//        for(int i = 10; i>=0; i-- ){
//            System.out.printf("%d x %d = %d\n" , x, i, x*i);
//        }
//        // problem 5
//        int n = 3;
//        int i = 1;
//        int factorial = 1;
//        while(i<=n){
//            factorial *= i;
//            i++;
//        }
//        System.out.println(factorial);
        // problem 6
        int n = 8;
        int sum = 0;
        for (int i =1; i<=10; i++){
            sum += n*i;
        }
        System.out.println(sum);





    }
}
