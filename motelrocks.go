package main

import (
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"
)

func getGoQueryDocument(url string )*goquery.Document{
	response, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}
	defer response.Body.Close()
	if response.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", response.StatusCode, response.Status)
	}
	document, err := goquery.NewDocumentFromReader(response.Body)
	if err != nil {
		log.Fatal(err)
	}
	return document
}

func Parse(url string){
	document := getGoQueryDocument(url)
	var links[] string
	document.Find("#main-nav .dropdown.has_sub_menu").Each(func(i int, selection *goquery.Selection){
		link, _ := selection.Find("a").Attr("href")
		 links = append(links, link)
	})
	allProductsLink := fmt.Sprintf("https://www.motelrocks.com%s", links[0])
	ParsePages(allProductsLink)
}

func ParsePages(url string){
	document := getGoQueryDocument(url)
	var pageNumbers[] string
	document.Find("#pagination a").Each(func(i int, selection *goquery.Selection){
		pageNumbers = append(pageNumbers, selection.Text())
	})
	lastPageNumber, _ := strconv.Atoi(pageNumbers[2])
	for i:= 1;i <= lastPageNumber; i++{
		lastPage := strconv.Itoa(lastPageNumber)
		url := fmt.Sprintf("https://www.motelrocks.com/collections/all?page=%s", lastPage)
		go ParseProducts(url)
	}
}

func ParseProducts(url string){
	document := getGoQueryDocument(url)
	var productLinks[] string
	document.Find(".product-info-inner").Each(func(i int, selection *goquery.Selection){
		link, _ := selection.Find("a").Attr("href")
		productLinks = append(productLinks, "https://www.motelrocks.com" + link)
	})
	for i:= 0; i< len(productLinks); i++{
		go ParseItem(productLinks[i])
	}
}

func ParseItem(url string) {
	document := getGoQueryDocument(url)
	fmt.Println(PopulateItems(document))
}

func PopulateItems(document *goquery.Document)map[string]string{
	motelrockItem := make(map[string]string)
	motelrockItem["name"] = ParseName(document)
	motelrockItem["price"] = ParsePrice(document)
	motelrockItem["size"] = ParseSize(document)
	motelrockItem["description"] = ParseDetails(document)
	motelrockItem["imgUrls"] = ParseImgUrls(document)
	motelrockItem["category"] = ParseCategory(document)
	return motelrockItem
}

func ParseName(doc *goquery.Document) string{
	var name string
	doc.Find("#product-description").Each(func(i int, selection *goquery.Selection){
		name = selection.Find("h1").Text()
	})
	return name
}

func ParsePrice(doc *goquery.Document) string{
	var price string
	doc.Find("#product-price").Each(func(i int, selection *goquery.Selection){
		price = selection.Find("span").Text()
	})
	return price
}

func ParseSize(doc *goquery.Document) string{
	var sizes[] string
	doc.Find(".swatch.clearfix div").Each(func(i int, selection *goquery.Selection){
		size := selection.Find("label").Text()
		cleanedSize := strings.TrimSpace(size)
		sizes = append(sizes, cleanedSize)
	})
	concatenatedSizes := strings.Join(sizes, ", ")
	return concatenatedSizes
}

func ParseDetails(doc *goquery.Document) string{
	var description string
	doc.Find("#details p").Each(func(i int, selection *goquery.Selection){
		description = selection.Find("span").Text()
	})
	return description
}

func ParseImgUrls(doc *goquery.Document) string{
	var imgUrl string
	var imgUrls[] string
	doc.Find(".slide a").Each(func(i int, selection *goquery.Selection){
		imgUrl,_ = selection.Find("img").Attr("src")
		imgUrls = append(imgUrls, fmt.Sprintf("https:%s", imgUrl))
	})
	concatenatedImgUrls := strings.Join(imgUrls, ", ")
	return concatenatedImgUrls
}

func ParseCategory(doc *goquery.Document) string{
	var categories[] string
	doc.Find("#breadcrumb a").Each(func(i int, selection *goquery.Selection){
		categories = append(categories, selection.Text())
	})
	return categories[1]
}

func main() {
	Parse("https://www.motelrocks.com")
	time.Sleep(time.Hour)
}

