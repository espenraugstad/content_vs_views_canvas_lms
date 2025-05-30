# Views vs Module Position

This code is used to examine the relationship between the position of items on the modules page in the Canvas LMS at the [University of Agder](https://uia.no), and the number of views. It is naturally expected that fewer students view the content of later modules. This may be due to students dropping out, or possibly there is less relevant information at the end. If the modules page is very long (which typically happens when the page is used to list tons of files), students may find it boring and not worth it, to scroll far enough to see the latest content. For fully online courses that are designed to guide students through pages and assignments in a linear fashion, the drop-off should be smaller than for physical classes where Canvas is used as a file repository.

# How to use

This tool requires two files. The first file can be obtained from Canvas' New Analytics Tool. Using this, go to the "Reports" tab and run a rapport for Course Activity. Download the csv file in the same folder as this file. This will be the activity file.

To get the other file, the script that follows along here can be used with a browser extension such as [Tampermonkey](https://www.tampermonkey.net/). Create a new script in this extension, and copy the code from the file "script.js". You may have to change the url in line 7 to match the url of your institutions Canvas installation. Note that it may also _not_ work if your institution has a custom Canvas setup. If it works, a button will be added on the modules page that says "List content". Clicking this will download a csv file. Make sure it is saved in the same folder as this file. This will be the content file.

Finally, in the Python script, add in the names of the activity and content files and run it. The result should be a scatter plot that show the position on the x-axis and number of views on the y-axis, along with a linear trend line.