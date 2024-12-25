package com.company;
import java.util.Scanner;


public class chapter_3_strings {
    public static void main(String[] args) {
       String name = "Harry";
       Scanner sc = new Scanner(System.in);
       String a = sc.next();
       String b = sc.next();
       int value = name.length();
       String lstring = name.toLowerCase();
       String usrting = name.toUpperCase();
       String tstring = name.trim();
       String sstring = name.substring(2);
       String rstring = name.replace('a' , 'J');
       String pstring = name.replace("a","qwerty");
       System.out.println(pstring);
       System.out.println(rstring);
       System.out.println(sstring);
       System.out.println(tstring);
       System.out.println(usrting);
       System.out.println(lstring);
       System.out.println(value);
       System.out.println(name.startsWith(a));
       System.out.println(name.endsWith(b));
       System.out.println(name.charAt(3));
       System.out.println(name.indexOf("rry"));
       String modifiedName = "harryp";
       System.out.println(modifiedName.indexOf("rry"));
       System.out.println(modifiedName.indexOf("rry", 4));
       System.out.println(modifiedName.lastIndexOf("rry", 4));
        System.out.println(modifiedName.equals("harryp"));
       System.out.println(modifiedName.equalsIgnoreCase("haRryp"));
       String na = new String("agrim");
       System.out.print("the name is : ");
       System.out.println(na);

       //Problem 1
       String n = "AGRIM JAIN";
       System.out.println(name.toLowerCase());
       //Problem 2
       String text = "A G R I M";
       System.out.println(text.replace(" ","_"));
       //Problem 3
       String letter = "Dear name , thanks a lot";
       System.out.println(letter.replace("name","agrim"));
       //Problem 4
       String given = "my  name is   agrim";
       System.out.println(given.indexOf("  "));
       System.out.println(given.indexOf("   "));
       //Problem 5
       String myLetter = " dear \n\t this java course is good\n thanks";
       System.out.println(myLetter);


    }
}
