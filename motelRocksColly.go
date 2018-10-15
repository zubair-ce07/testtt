package main

import (
	"encoding/csv"
	"fmt"
	"github.com/gocolly/colly"
	"log"
	"os"
	"strconv"
	"strings"
)

type item struct {
	name string
	price string
	Size string
	description string
	imgUrls string
	category string
}

func parseSizePrice(priceSize[] string, size[] string, price string){
	for i := 0; i < len(priceSize); i++{
		sizePriceSplit := strings.Split(priceSize[i], "-")
		size = append(size, sizePriceSplit[0])
		price = sizePriceSplit[1]
	}
}

func main() {
	parse := colly.NewCollector(
		colly.AllowedDomains("www.motelrocks.com"),
	)
	pagination := parse.Clone()
	parseProducts := parse.Clone()
	parseItem := parse.Clone()

	var name string
	var currency string
	var priceSize[] string
	var price string
	var size[] string
	var descriptions[] string
	var imgUrls[] string
	var links[] string
	var pageNumbers[] string
	var collectionLinks[] string
	var categories[] string
	var items[] item
	
	parse.OnHTML("#main-nav .dropdown.has_sub_menu", func(tag *colly.HTMLElement){
		collectionLinks = append(collectionLinks, tag.ChildAttr("a", "href"))
	})

	parse.OnHTML("#main-nav", func(target *colly.HTMLElement){
		pagination.Visit("https://www.motelrocks.com" + collectionLinks[0])
	})

	pagination.OnHTML("#pagination a", func(tag *colly.HTMLElement){
		pageNumbers = append(pageNumbers, tag.Text)
	})

	pagination.OnHTML("#pagination", func(tag *colly.HTMLElement){
		lastPageNumber, _ := strconv.Atoi(pageNumbers[2])
		for i := 1; i < lastPageNumber; i++{
			parseProducts.Visit("https://www.motelrocks.com/collections/all?page=" + strconv.Itoa(i))
		}
	})

	parseProducts.OnHTML(".product-info-inner", func(tag *colly.HTMLElement) {
		links = append(links, "https://www.motelrocks.com" + tag.ChildAttr("a", "href"))
		for i := 0; i < len(links); i++{
			parseItem.Visit(links[i])
		}
	})

	parseItem.OnHTML("#product-description", func(tag *colly.HTMLElement) {
		name = tag.ChildText("h1")
		currency = tag.ChildAttr("meta", "content")
	})

	parseItem.OnHTML("#details p", func(tag *colly.HTMLElement) {
		descriptions = append(descriptions, tag.ChildText("span"))

	})

	parseItem.OnHTML(".slide a ", func(tag *colly.HTMLElement) {
		imgUrls = append(imgUrls,  "https:" + tag.ChildAttr("img", "src"))
	})

	parseItem.OnHTML("#breadcrumb a", func(tag *colly.HTMLElement) {
		categories = append(categories, tag.Text)
	})

	parseItem.OnHTML(".select", func(tag *colly.HTMLElement) {
		priceSize = append(priceSize, tag.ChildText("option"))
	})

	parseItem.OnHTML(".slide", func(tag *colly.HTMLElement) {
		parseSizePrice(priceSize, size, price)
		sizes := strings.Join(size, ", ")
		imgUrls := strings.Join(imgUrls, ", ")
		description := strings.Join(descriptions, ", ")
		motelItem := item{name, price, sizes , description, imgUrls, categories[1]}
		items = append(items, motelItem)
		fmt.Println(motelItem.name + " " + motelItem.price + " " + motelItem.Size + " " + motelItem.category + " " +
			motelItem.imgUrls + " " + motelItem.description )
	})

	parse.Visit("https://www.motelrocks.com/")

	fileName := "motelrocks.csv"
	file, err := os.Create(fileName)
	if err != nil {
		log.Fatalf("Cannot create file %q: %s\n", fileName, err)
		return
	}
	defer file.Close()
	writer := csv.NewWriter(file)
	defer writer.Flush()
	for i:= 0; i < len(items); i++{
		writer.Write([]string{"Name: " + items[i].name, "Price: "+ items[i].price, "Sizes " + items[i].Size ,
		"Image Urls: " + items[i].imgUrls, "Category: " + items[i].category, "Description: " + items[i].description})
	}
}
