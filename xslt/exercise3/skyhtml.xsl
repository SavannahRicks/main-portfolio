<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.w3.org/1999/xhtml"
    version="3.0">
    <xsl:output method="xhtml" html-version="5" omit-xml-declaration="yes" 
        include-content-type="no" indent="yes"/>
    
    <xsl:template match="/">
        
        <html>
            <head>
                <title>Skyrim</title>
                <link rel="stylesheet" type="text/css" href="style.css"/>
            </head>
            <body>
                <xsl:apply-templates select="skyrim"></xsl:apply-templates>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="title">
        <h1><xsl:apply-templates/></h1>
    </xsl:template>
    
    <xsl:template match="attribution">
        <p><xsl:apply-templates/></p>
    </xsl:template>
    
    <xsl:template match="subtitle">
        <h2><xsl:apply-templates/></h2>
    </xsl:template>
    
    <xsl:template match="paragraph">
        <p><xsl:apply-templates/></p>
    </xsl:template>
    
    <!-- ************************************************************************ -->
    
    <xsl:template match="QuestEvent">
        <span class="event"><xsl:apply-templates/></span>
    </xsl:template>
    
    <xsl:template match="QuestItem">
        <span class="item"><xsl:apply-templates/></span>
    </xsl:template>
    
    <xsl:template match="character">
        <span class="{preceding::character[@id = current()/@ref]/@alignment}"><xsl:apply-templates/></span>
    </xsl:template>
    
    <xsl:template match="epithet">
        <span class="epithet"><xsl:apply-templates/></span>
    </xsl:template>
    
    <xsl:template match="faction"> <!-- I couldn't figure out a way to specify alignmnet factions to their specific border colors. -->
        <span class="faction"><xsl:apply-templates/></span>
    </xsl:template>
    
    <xsl:template match="location">
        <span class="location"><xsl:apply-templates/></span>
    </xsl:template>
</xsl:stylesheet>