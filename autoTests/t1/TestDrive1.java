package t1;

import java.awt.AWTException;
import java.awt.event.KeyEvent;
import java.awt.Robot;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.openqa.selenium.By;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class TestDrive1 {

    private ArrayList<String> linkList = new ArrayList<String>();
    private List<WebElement> linkElements;
    private ArrayList<String> titleList = new ArrayList<String>();
    private String baseUrl;

    public static void main(String[] args) {
        System.setProperty("webdriver.chrome.driver", "D:\\QA_class_1"
                + "\\Selenium\\chromedriver_win32\\chromedriver.exe");
        WebDriver driver = new ChromeDriver();

        String[] engUrl = new String[4];
        engUrl[0] = "http://a90378u5.beget.tech/website2ENGLISH.html";
        engUrl[1] = "http://a90378u5.beget.tech/calculatorENGLISH.html";
        engUrl[2] = "http://a90378u5.beget.tech/riddleENGLISH.html";
        engUrl[3] = "http://a90378u5.beget.tech/guessingGameENGLISH.html";
        
        String[] rusUrl = new String[4];
        rusUrl[0] = "http://a90378u5.beget.tech/website2.html";
        rusUrl[1] = "http://a90378u5.beget.tech/calculatorPage.html";
        rusUrl[2] = "http://a90378u5.beget.tech/riddle.html";
        rusUrl[3] = "http://a90378u5.beget.tech/guessingGame.html";
        
        for (int i = 0; i < 4; i++) {
            TestDrive1[] test = new TestDrive1[4];
            RusPage[] page = new RusPage[4];
            page[i] = new RusPage(i);
            //page[i].setPageTitle(titles[i]);
            page[i].setLinks();
            page[i].addLinks();
            page[i].setTitles();
            page[i].addTitles();

            test[i] = new TestDrive1();
            test[i].setUrl(rusUrl[i]);
            driver.get(rusUrl[i]);

            test[i].pressEsc();
            test[i].threadToSleep();

            test[i].setLinks(driver);
            test[i].setTitles(driver, test[i]);

            test[i].compareLinks(page[i].getLinks());
            test[i].compareTitles(page[i].getTitles());
        }
        
        for (int i = 0; i < 4; i++) {
            TestDrive1[] test = new TestDrive1[4];
            EngPage[] page = new EngPage[4];
            page[i] = new EngPage(i);
            //page[i].setPageTitle(titles[i]);
            page[i].setLinks();
            page[i].addLinks();
            page[i].setTitles();
            page[i].addTitles();

            test[i] = new TestDrive1();
            test[i].setUrl(engUrl[i]);
            driver.get(engUrl[i]);

            test[i].pressEsc();
            test[i].threadToSleep();

            test[i].setLinks(driver);
            test[i].setTitles(driver, test[i]);

            test[i].compareLinks(page[i].getLinks());
            test[i].compareTitles(page[i].getTitles());
        }
    }

    public void setUrl(String s) {
        baseUrl = s;
    }

    public String getUrl(int i) {
        return baseUrl;
    }

    public void setLinks(WebDriver d) {
        linkElements = d.findElements(By.tagName("a"));
        for (int i = 0; i < linkElements.size(); i++) {
            String text = linkElements.get(i).getText();
            linkList.add(text);
        }
    }

    public void setTitles(WebDriver d, TestDrive1 t) {
        for (int i = 0; i < linkElements.size(); i++) {
            linkElements.get(i).click();
            String title = d.getTitle();
            titleList.add(title);
            d.get(baseUrl);
            String s = d.getTitle();
            if (s.equals("Mock-Up Web Site") || s.equals("Mock-Up Web Site ENG")) {
                t.threadToSleep();
                t.pressEsc();
                t.threadToSleep();
            }
            linkElements = d.findElements(By.tagName("a"));
        }
    }

    public void compareLinks(ArrayList<String> l) {
        for (int i = 0; i < linkList.size(); i++) {
            if (l.get(i).equals(linkList.get(i))) {
                System.out.println("Текст ссылки #" + (i+1) + ": работает");
            } else {
                System.out.println("Текст ссылки #" + (i+1) + ": НЕ работает");
            }
        }
        System.out.println("");
    }

    public void compareTitles(ArrayList<String> t) {
        for (int i = 0; i < titleList.size(); i++) {
            if (t.get(i).equals(titleList.get(i))) {
                System.out.println("Заголовок страницы #" + (i+1) + ": работает");
            } else {
                System.out.println("Заголовок страницы #" + (i+1) + ": НЕ работает");
            }
        }
        System.out.println("");
    }

    public void pressEsc() {
        try {
            Robot r = new Robot();
            r.keyPress(KeyEvent.VK_ESCAPE);
            r.keyRelease(KeyEvent.VK_ESCAPE);
        } catch (AWTException ex) {
            Logger.getLogger(TestDrive1.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    public void threadToSleep() {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException ex) {
            Logger.getLogger(TestDrive1.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

}

