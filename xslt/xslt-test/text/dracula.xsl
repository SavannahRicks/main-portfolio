<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math" exclude-result-prefixes="xs math"
    version="3.0">

    <xsl:output method="xhtml" html-version="5" omit-xml-declaration="yes"/>
    <!-- **************************************************************************-->
    <!-- 2022-11-17 ebb: This XSLT starter file is for the XSLT test in DIGIT 110. 
    Do not alter the stylesheet root element or the output line. 
    
   Your task is to transform the source XML document of Bram Stoker's novel Dracula into HTML with a 
   table of contents linked to a reading view, and styled with CSS. Your XSLT code needs to 
   * process one source XML file and output one valid and well-formed HTML file;
   * contain an HTML table  for the table of contents featuring:
        * each chapter heading
        * each chapter's distinct sorted locations
        * each chapter's distinct sorted technologies;
        
   * contain internal links from the chapter headings in the table of contents to the chapter headings;
   * contain span elements in the reading view to stylize the locations and technologies mentioned. 
   * Prepare CSS to style your HTML. The XSLT should output the CSS link line to your CSS file accurately. 
   
   
    -->
    <!-- **************************************************************************-->



    <xsl:template match="/">
        <html>
            <head>
                <title>Dracula</title>
                <link rel="stylesheet" type="text/css" href="style.css"/>
            </head>


            <body>
                <h1 id="top"><xsl:apply-templates select="//title"/></h1>

                <section id="contents">
                    <table class="tb">
                        <tr>
                            <th>Chapter Number</th>
                            <th>Locations mentioned</th>
                            <th>Tech mentioned</th>
                        </tr>
                        <xsl:apply-templates select="//chapter" mode="contents"/>
                    </table>
                </section>


                <section id="readingView" >
                    <xsl:apply-templates select="//chapter"/>
                </section>

            </body>
        </html>
    </xsl:template>



    <xsl:template match="chapter" mode="contents">
        <tr>
            <td class="col1">
                <!-- Column 1 -->
                <a href="#ch{count(preceding-sibling::chapter)+1}">
                    <xsl:apply-templates select="heading ! string()"/>
                </a>
            </td>
            <td class="col2">
                <!-- Column 2 -->
                <xsl:apply-templates
                    select=".//location ! normalize-space() => distinct-values() => sort() => string-join(', ')"
                />
            </td>
            <td class="col3">
                <!-- Column 3 -->
                <xsl:apply-templates
                    select=".//tech ! normalize-space() => distinct-values() => sort() => string-join(', ')"
                />
            </td>
        </tr>
    </xsl:template>
    
    <xsl:template match="location">
        <span class="loc"><xsl:apply-templates select="location"/></span>
    </xsl:template>
    <xsl:template match="time">
        <span class="time"><xsl:apply-templates select="time"/></span>
    </xsl:template>
    <xsl:template match="date">
        <span class="date"><xsl:apply-templates select="date"/></span>
    </xsl:template>
    <xsl:template match="tech">
        <span class="tech"><xsl:apply-templates select="tech"/></span>
    </xsl:template>






    <xsl:template match="chapter">
        <!-- There might be a better way in doing this column lol -->
        <h2 id="ch{count(preceding-sibling::chapter)+1}">
            <xsl:apply-templates/>
        </h2>
    </xsl:template>
    <xsl:template match="heading">
        <h2>
            <xsl:apply-templates/>
        </h2>
    </xsl:template>
    <xsl:template match="p">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>

</xsl:stylesheet>
