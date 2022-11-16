<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns="http://www.w3.org/1999/xhtml"
    version="3.0">

    <xsl:output method="xhtml" html-version="5" omit-xml-declaration="yes" include-content-type="no"
        indent="yes"/>

    <xsl:variable name="travelColl" as="document-node()+"
        select="collection('xml-letters/?select=*.xml')"/>

    <xsl:template match="/"><!-- ebb: Set up the XSLT to run against any single XML file, so this 
    tmemplate has a document node to match on-->
        <html>
            <head>
                <title>Behrend Travel Letters</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <link rel="stylesheet" type="text/css" href="web-out/webstyle.css"/>
            </head>
            <body>
                <h1>Behrend's Travel Adventures in France</h1>
                <section id="toc">
                    <h2>Contents</h2>
                    <table>
                        <tr>
                            <th>Letter Date</th>
                            <th>People Mentioned</th>
                            <th>Places Mentioned</th>
                        </tr>
                        
                        <xsl:apply-templates select="$travelColl//letter" mode="toc"/>
                    </table>
                </section>

                <section id="fulltext">
                    <xsl:apply-templates select="$travelColl//letter"></xsl:apply-templates>
                </section>
            </body>
        </html>
    </xsl:template>
    
    <!-- ************************************************* -->
    <!-- ebb: TOC mode templates for the table of contents -->
    <!-- ************************************************* -->
   
   <xsl:template match="letter" mode="toc">
       <tr>
           <td><xsl:apply-templates select="@xml:id"/></td>
           <td>
               <xsl:apply-templates select="//letter//persName ! substring(., 1)"/></td>
           <td><xsl:apply-templates select="//letter//placeName ! substring(., 1)"/></td>
           
       </tr>
   </xsl:template>

    <!-- ************************************************* -->
    <!-- ebb: templates for outputting the text of the letters -->
    <!-- ************************************************* -->
    
    <xsl:template match="letter">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    <xsl:template match="figure">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    <xsl:template match="dateLine">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    <xsl:template match="letter[@id='Brussels-1955-07-26']/placeName">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>

</xsl:stylesheet>
