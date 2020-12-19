package com.tribos;

import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.chrome.ChromeDriver;

import static org.junit.Assert.assertEquals;

public class TribosTests {

    private static WebDriver driver;
    private String baseUrl = "http://localhost:3000/";

    @BeforeClass
    public static void inicializarBrowser() {
        System.setProperty("webdriver.chrome.driver", "chromedriver");
        driver = new ChromeDriver();
    }

    @Before
    public void inicializarTeste() {
        driver.manage().deleteAllCookies();
    }

    @Test
    public void testarCadastro() throws InterruptedException {
        driver.get(this.baseUrl + "register");
        WebElement element = driver.findElement(By.name("email"));
        Thread.sleep(1000L);
        element.sendKeys("testerson@email.com");
        Thread.sleep(2000L);

        element = driver.findElement(By.name("user_name"));
        element.sendKeys("Testerson");
        Thread.sleep(2000L);

        element = driver.findElement(By.name("birthday"));
        element.sendKeys("01012000");
        Thread.sleep(2000L);

        element = driver.findElement(By.name("password"));
        element.sendKeys("senhaforte");
        Thread.sleep(2000L);

        Select select = new Select(driver.findElement(By.name("gender")));
        select.selectByVisibleText("Outro");

        element = driver.findElement(By.tagName("form"));
        element.submit();
        Thread.sleep(2000L);

        driver.switchTo().alert();
        String textoDoAlert = driver.switchTo().alert().getText();
        driver.switchTo().alert().dismiss();

        assertEquals(textoDoAlert, "Cadastro realizado com sucesso");
    }

    @Test
    public void testarCadastroComVazio() throws InterruptedException {
        driver.get(this.baseUrl + "register");
        WebElement element = driver.findElement(By.name("email"));
        Thread.sleep(1000L);
        element.sendKeys("eobred@email.com");
        Thread.sleep(2000L);

        element = driver.findElement(By.name("birthday"));
        element.sendKeys("01012000");
        Thread.sleep(2000L);

        element = driver.findElement(By.name("password"));
        element.sendKeys("senhaforte");
        Thread.sleep(2000L);

        Select select = new Select(driver.findElement(By.name("gender")));
        select.selectByVisibleText("Outro");

        element = driver.findElement(By.tagName("form"));
        element.submit();
        Thread.sleep(2000L);

        driver.switchTo().alert();
        String textoDoAlert = driver.switchTo().alert().getText();
        driver.switchTo().alert().dismiss();

        assertEquals(textoDoAlert, "Preencha todos os campos!");
    }


    @AfterClass
    public static void tearDownTest(){
        driver.quit();
    }

}
