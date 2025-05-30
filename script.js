// ==UserScript==
// @name         Canvas Modules Content Numbered
// @namespace    http://tampermonkey.net/
// @version      2025-05-29
// @description  Retrieve a numbered list of the content in the modules in Canvas
// @author       Espen Raugstad
// @match        https://uia.instructure.com/courses/*/modules
// @icon         https://www.google.com/s2/favicons?sz=64&domain=instructure.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Your code here...
    /***** GLOBAL CONSTANTS AND VARIABLES *****/
    const BASE_URL = "https://uia.instructure.com";
    const MODULES_API = `/api/v1/courses/${ENV.course_id}/modules`;

    // Start
    const observer = new MutationObserver((mutations, observer) => {
        for(const mutation of mutations){
            const navBar = document.querySelector(".header-bar-right__buttons");
            if(navBar){
                observer.disconnect();
                addButton(navBar);
                return;
            }
        }
    });

    observer.observe(document.body, {childList: true, subtree: true});

    function addButton(navbar){
        const addGetListButton = document.createElement("button");
        addGetListButton.classList.add("btn", "btn-info");
        addGetListButton.style.marginLeft = "1rem";
        addGetListButton.innerText = "List content";
        navbar.appendChild(addGetListButton);
        addGetListButton.addEventListener("click", getContent);
    }

    async function getContent(){
        console.log("Hi")
        // Get modules
        const modules = await getModules(BASE_URL + MODULES_API, []);
        if(modules.length <= 0){
            return;
        }
        let allItems = [];
        for(const module of modules){
            if(module.items_count != 0){
                console.log(module);
                let currentItems = await getCurrentItems(module.items_url);
                allItems = allItems.concat(currentItems);
            }
        }
        console.log(allItems);
        let csvData = prepareData(allItems);
        if(csvData){
            downloadData(csvData);
        }
    }

    async function getModules(url, modules = []){
        try{
            let res = await fetch(url);
            if(res.status != 200){
                throw new Error("Unable to get modules. Status " + res.status);
            }
            let data = await res.json();
            modules = modules.concat(data);
            let nextLink = findNextLink(res);
            if(nextLink){
                return await getModules(nextLink, modules);
            } else{
                return modules;
            }
        }
        catch(err){
            console.error(err);
        }
    }

    async function getCurrentItems(url, items = []){
        try{
            let res = await fetch(url);
            if(res.status != 200){
                throw new Error("Unable to get module items. Status " + res.status);
            }
            let data = await res.json();
            items = items.concat(data);
            let nextLink = findNextLink(res);
            if(nextLink){
                return await getCurrentItems(nextLink, items);
            } else{
                return items;
            }
        }
        catch(err){
            console.error(err);
        }
    }

    function prepareData(data){
        console.log(data);
        let csv = "Position,Title,Type,Published\n";
        for(let i = 0; i < data.length; i++){
            csv += `${i},${data[i].title},${data[i].type},${data[i].published ? "Published" : "Not published"}\n`;
        }
        return csv;
    }

    function downloadData(data){
        const blob = new Blob(["\uFEFF"+data], { type: 'text/csv;charset=UTF-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        let courseName = "";
        try{
            courseName = ENV.current_context.name;
        } catch(error){
            console.error("Unable to locate course name: ", error);
            courseName = "-";
        }
        a.download = "Content_" + courseName + '.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    /***** UTILITY FUNCTIONS *****/
    function findNextLink(results){
        let responseHeaders = [...results.headers];
        let linkHeader = responseHeaders.find((el) => el[0].toLowerCase() === "link");
        let textArray = linkHeader[1].split(",");
        // Go through and see if we find a next link
        for(const link of textArray){
            let [url, rel] = link.split(";");
            if(rel.includes("next")){
                // Remove the < and > from start and end.
                return url.substring(1,url.length - 1);
            }
        }
        return false; // No next-link was found.
    }


})();