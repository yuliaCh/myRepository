
package t1;

import java.util.ArrayList;

public class EngPage {
    private String baseTitle;
    private ArrayList<String> pageLinks = new ArrayList<String>();
    private ArrayList<String> pageTitles = new ArrayList<String>();
    private String[] part;
    
    public EngPage(int i) {
        switch (i) {
            case 0:
                System.out.println("Тестируется страница: Главная - АНГЛ");
                baseTitle = "Mock-Up Web Site ENG";
                break;
            case 1:
                System.out.println("Тестируется страница: Калькулятор - АНГЛ");
                baseTitle = "Mock-Up - Calculator ENG";
                break;
            case 2:
                System.out.println("Тестируется страница: Загадки - АНГЛ");
                baseTitle = "Mock-Up - Riddles ENG";
                break;
            case 3:
                System.out.println("Тестируется страница: Игра Угадайка - АНГЛ");
                baseTitle = "Mock-Up - Guessing Game ENG";
                break;
        }
    }
    
    public void setLinks() {
        pageLinks.add("Home");
        pageLinks.add("Calculator");
        pageLinks.add("Riddles");
        pageLinks.add("Guessing Game");
        pageLinks.add("Русский");
    }    
    
    public void addLinks() {
        pageLinks.add("Русский");
    }
    
    public ArrayList<String> getLinks(){
        return pageLinks;
    }
    
    public void setTitles() {
        part = baseTitle.split(" ENG");
        pageTitles.add("Mock-Up Web Site ENG");
        pageTitles.add("Mock-Up - Calculator ENG");
        pageTitles.add("Mock-Up - Riddles ENG");
        pageTitles.add("Mock-Up - Guessing Game ENG");       
        pageTitles.add(part[0]);
    }
    public ArrayList<String> getTitles(){
        return pageTitles;
    }
    
    public void addTitles() {
        pageTitles.add(part[0]);
    }    
}
