package org.brnvrn;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * The tool "Java bean"
 * Is exported as JSON
 */
public class Tool {

    private String category;
    private String name;
    private String description; // Might contain HTML
    private String descriptionText;
    private String url;
    private String url_src;
    private String license;
    private Set<String> language = new HashSet<>(4);
    private Set<String> author = new HashSet(4);
    private Set<String> theme = new HashSet(10);
    private String compatibility;
    private boolean obsolete;
    private String verified;
    private String last_update;
    private boolean nonUniqueName;

    public Tool() {};

    public Tool(boolean isObsolete) {
        obsolete = isObsolete;
    }

    public void clearLanguage() {
        language.clear();
    }

    public void clearAuthor() {
        author.clear();
    }

    public void clearTheme() {
        theme.clear();
    }

    public boolean addAuthor(String newAuthor) {
        author.add(newAuthor);
        return true;
    }
    public boolean addAuthor(String[] newAuthor) {
        for (String aut: newAuthor) {
            author.add(aut.trim());
        }
        return true;
    }
    public boolean addLanguage(String newLang) {
        language.add(newLang.trim());
        return true;
    }
    public boolean addTheme(String newTheme) {
        theme.add(newTheme.trim());
        return true;
    }

    /**
     * TODO, could use the JSON mapper directly
     * @return
     */
    @Override
    public String toString() {
        return "Tool{" +
                "category='" + category + '\'' +
                ", name='" + name + '\'' +
                ", description='" + description + '\'' +
                ", url='" + url + '\'' +
                ", url_src='" + url_src + '\'' +
                ", license='" + license + '\'' +
                ", language=" + language +
                ", author=" + author +
                ", theme=" + theme +
                ", compatibility='" + compatibility + '\'' +
                ", obsolete=" + obsolete +
                ", verified='" + verified + '\'' +
                ", last_update='" + last_update + '\'' +
                '}';
    }

    public String getUrl_src() {
        return url_src;
    }

    public void setUrl_src(String url_src) {
        this.url_src = url_src;
    }

    public String getLicense() {
        return license;
    }

    public void setLicense(String license) {
        this.license = license;
    }

    public Set<String> getLanguage() {
        return language;
    }

    public void setLanguage(Set<String> language) {
        this.language = language;
    }

    public Set<String> getAuthor() {
        return author;
    }

    public void setAuthor(Set<String> author) {
        this.author = author;
    }

    public Set<String> getTheme() {
        return theme;
    }

    public void setTheme(Set<String> theme) {
        this.theme = theme;
    }

    public String getCompatibility() {
        return compatibility;
    }

    public void setCompatibility(String compatibility) {
        this.compatibility = compatibility;
    }

    public boolean isObsolete() {
        return obsolete;
    }

    public void setObsolete(boolean obsolete) {
        this.obsolete = obsolete;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }


    public String getVerified() {
        return verified;
    }

    public void setVerified(String verified) {
        this.verified = verified;
    }

    public String getLast_update() {
        return last_update;
    }

    public void setLast_update(String last_update) {
        this.last_update = last_update;
    }

    public String getDescriptionText() {
        return descriptionText;
    }

    public void setDescriptionText(String descriptionText) {
        this.descriptionText = descriptionText;
    }
}
