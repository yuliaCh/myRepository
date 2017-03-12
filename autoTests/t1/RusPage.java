
package t1;

import java.util.ArrayList;

public class RusPage {
    private String baseTitle;
    private ArrayList<String> pageLinks = new ArrayList<String>();
    private ArrayList<String> pageTitles = new ArrayList<String>();
    
    public RusPage(int i) {
        switch (i) {
            case 0:
                System.out.println("Тестируется страница: Главная - РУС");
                baseTitle = "Mock-Up Web Site";
                break;
            case 1:
                System.out.println("Тестируется страница: Калькулятор - РУС");
                baseTitle = "Mock-Up - Calculator";
                break;
            case 2:
                System.out.println("Тестируется страница: Загадки - РУС");
                baseTitle = "Mock-Up - Riddles";
                break;
            case 3:
                System.out.println("Тестируется страница: Игра Угадайка - РУС");
                baseTitle = "Mock-Up - Guessing Game";
                break;
        }
    }
    
    public void setLinks() {
        pageLinks.add("Главная");
        pageLinks.add("Калькулятор");
        pageLinks.add("Загадки");
        pageLinks.add("Игра Угадайка");
        pageLinks.add("English");
    }    
    
    public void addLinks() {
        pageLinks.add("English");
    }
    
    public ArrayList<String> getLinks(){
        return pageLinks;
    }
    
    public void setTitles() {
        pageTitles.add("Mock-Up Web Site");
        pageTitles.add("Mock-Up - Calculator");
        pageTitles.add("Mock-Up - Riddles");
        pageTitles.add("Mock-Up - Guessing Game");       
        pageTitles.add(baseTitle + " ENG");
    }
    public ArrayList<String> getTitles(){
        return pageTitles;
    }
    
    public void addTitles() {
        pageTitles.add(baseTitle + " ENG");
    } 
      
}
