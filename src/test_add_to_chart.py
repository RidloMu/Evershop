import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin:
    @pytest.mark.add_to_chart
    def test_add_to_chart(self):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://demo.evershop.io/mix-and-match-chuck-taylor-all-star-118")
        driver.implicitly_wait(2)

        # input jumlah sepatu
        shoe_qty = '3'
        qty = driver.find_element(By.XPATH, "//input[@name='qty']")
        qty.clear()
        qty.send_keys(shoe_qty)

        # Pilih ukuran sepatu
        shoe_size = 'L'
        size = driver.find_element(By.XPATH, f"//a[normalize-space()='{shoe_size}']")
        size.click()

        # Pilih warna sepatu
        shoe_colour = 'Brown'
        colour = driver.find_element(By.XPATH, f"//a[contains(text(),'{shoe_colour}')]")
        colour.click()
        time.sleep(1)

        # Add to char
        button_addtochart = driver.find_element(By.XPATH, "//button[@class='button primary outline']")
        button_addtochart.click()

        # Validasi muncul pop up
        try:
            pop_up = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='toast-mini-cart']"))
            )
            assert pop_up.is_displayed(), "Pop-up is not displayed"
            print("Pop-up is displayed")

        except AssertionError as e:
            print(e)

        # Validasi produk pada pop up sama
        name_produk = driver.find_element(By.XPATH, "//h1[@class='product-single-name']").text
        produk_confirm = driver.find_element(By.XPATH, "//div[@class='name']").text
        assert produk_confirm.lower() == name_produk.lower(), "Produk tidak sama"
        print("Produk sama")

        # validasi qty sama dengan yang di input sebelumnya
        pop_up_isi = driver.find_element(By.XPATH, "//div[@class='item-info flex justify-between']")
        child_divs = pop_up_isi.find_elements(By.XPATH, ".//div")

        # Pastikan jumlah elemen div dalam parent div adalah 2
        assert len(child_divs) == 2, "Number of div elements inside parent div is not equal to 2"

        # Jika assert berhasil, pesan ini tidak akan ditampilkan
        print("Number of div elements inside parent div is equal to 2")

        view_cart = driver.find_element(By.XPATH, "//a[@class='add-cart-popup-button']")
        view_cart.click()

        get_url = driver.current_url
        assert get_url == "https://demo.evershop.io/cart", "link beda"

        print("Link sama")

        time.sleep(5)