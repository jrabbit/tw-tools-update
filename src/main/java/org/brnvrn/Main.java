package org.brnvrn;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonToken;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.MappingJsonFactory;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

import static java.time.temporal.ChronoUnit.YEARS;

/**
 * Inputs:
 *  - the previous json data
 *  - the GitHub search (HTTP request or local files)
 * For each GitHub_repo_found
 *    if match previous data
 *        update previous data
 *    else
 *        add to previous data
 *
 */
public class Main {
    public static void main(String[] args) throws Exception {


        ClassLoader classloader = Thread.currentThread().getContextClassLoader();
        InputStream dataTools = classloader.getResourceAsStream("data-tools.json");

        ObjectMapper mapper = new ObjectMapper();
        mapper.enable(SerializationFeature.INDENT_OUTPUT);
        List<Tool> tools = mapper.readValue(dataTools, new TypeReference<List<Tool>>() {});
        System.out.println("Loaded " + tools.size() +" old tools.");

        JsonFactory f = new MappingJsonFactory();
        JsonParser jp = null;
        int nbGithubRequests = 0;
        boolean hasMoreResult = true;
        while (hasMoreResult ) {
            String fileName = "github."+ (++nbGithubRequests) +".100.json";
            System.out.println("Loading results: " + fileName);
            try {
                InputStream github1 = classloader.getResourceAsStream(fileName);
                jp = f.createParser(github1);
            } catch (IOException e) {
                e.printStackTrace();
            }
            hasMoreResult = parseBatchOfGithubResults(jp, tools);
        }
        // write the new updated data
        try {
            mapper.writeValue( new FileOutputStream("data-tools.json"), tools );
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Parse a GitHub response, return true if there was results in it.
     * @param jp
     * @param tools
     * @return
     * @throws Exception
     */
    private static boolean parseBatchOfGithubResults(JsonParser jp, List<Tool> tools) throws Exception {
        JsonToken current;
        current = jp.nextToken();
        boolean hasResults = false;
        if (current != JsonToken.START_OBJECT) {
            throw new Exception("Error: root should be object: quiting.");
        }
        while (jp.nextToken() != JsonToken.END_OBJECT) {
            String fieldName = jp.getCurrentName();
            current = jp.nextToken();
            if (fieldName.equals("items")) {
                if (current == JsonToken.START_ARRAY) {
                    // For each of the item in the array
                    while (jp.nextToken() != JsonToken.END_ARRAY) {
                        hasResults = true;
                        // read the record into a tree model,
                        // this moves the parsing position to the end of it
                        JsonNode node = jp.readValueAsTree();
                        // And now we have random access to everything in the object
                        System.out.print("Process name: " + node.get("full_name").asText() + " ... ");
                        if (!isToolUpdate(node, tools)) {
                            addTools(node, tools);
                            System.out.println("Added.");
                        }
                    }
                } else {
                    System.out.println("Error: records should be an array: skipping.");
                    jp.skipChildren();
                }
            } else {
                jp.skipChildren();
            }
        }
        return hasResults;
    }

    /**
     * Add a new tool to the list of existing tools
     *  Todo: Category???
     * @param node
     * @param tools
     */
    private static void addTools(JsonNode node, List<Tool> tools) {
        Tool tool = new Tool();
        tool.setName(node.get("name").asText());
        tool.setCategory("Unknown");
        updateTool(node, tool);
        tools.add(tool);
    }

    /**
     * Is the tool previously existing?  Then update and return yes
     * @param node
     * @param tools
     * @return
     */
    private static boolean isToolUpdate(JsonNode node, List<Tool> tools) throws Exception {
        String name = node.get("name").asText();
        List<Tool> matches = tools.stream().filter(e -> e.getName().equalsIgnoreCase(name)).collect(Collectors.toList());
        if (matches.size() == 0)  return false;
        if (matches.size()  > 1) System.out.print("(Warning: Please check possible duplicates in previous data !) ");

        int matchesNumb = 0;
        for (Tool tool : matches) {
            String url_src = tool.getUrl_src();
            if (url_src != null && url_src.equals(node.get("html_url").asText())) {
                if (++matchesNumb >1)  {
                    throw new Exception("Error: at least 2 projects have the same name and URL in previous data: "+ name +" !");
                };
                updateTool(node, tool);
                System.out.println("Updated.");
            }
        }
        if (matchesNumb == 0)  {
            System.out.print("(Warning: Please check duplicates !  May be on GitHub, but the source URL does not link to GitHub.) ");
            return false;
        } else {
            return true;
        }
    }

    /**
     * Update all field but the category ...
     * @param node
     * @param tool
     */
    private static void updateTool(JsonNode node, Tool tool) {
        tool.setDescription(node.get("description").asText());
        tool.setDescriptionText(node.get("description").asText());
        tool.setUrl(node.get("homepage").asText().isEmpty() ? node.get("html_url").asText() : node.get("homepage").asText());
        tool.setUrl_src(node.get("html_url").asText());
        tool.clearAuthor();
        tool.addAuthor(node.get("owner").get("login").asText());
        tool.clearLanguage();
        tool.addLanguage(node.get("language").asText());
        tool.setLast_update(node.get("updated_at").asText().substring(0, "2015-12-34".length()));
        tool.setVerified(LocalDate.now().toString());
        tool.setObsolete(LocalDate.parse(tool.getLast_update()).isBefore(LocalDate.now().minus(3, YEARS)));
        bestEffortTheme(tool);
        // TODO find the license info ...
        // TODO Make further requests to get full author name and collaborators
    }

     /*
    As an extra ...
    Tries to extract theme info from the description
    MUST be called after the description is set!
     */
    private static void bestEffortTheme(Tool tool) {
        if (tool.getDescription().contains("GUI")
                || tool.getDescription().contains("GTK")
                || tool.getDescription().toLowerCase().contains("graphic")
                ) {
            tool.addTheme("GUI");
        }
        if (tool.getDescription().contains("XMPP")) {
            tool.addTheme("XMPP");
        }
        if (tool.getDescription().toLowerCase().contains("android")) {
            tool.addTheme("Android");
        }
        if (tool.getDescription().toLowerCase().contains("osx")
                || tool.getDescription().toLowerCase().contains("os x")) {
            tool.addTheme("OSX");
        }
        if (tool.getDescription().toLowerCase().contains("web")) {
            tool.addTheme("Web");
        }
        if (tool.getDescription().toLowerCase().contains("vim")) {
            tool.addTheme("Vim");
        }
        if (tool.getDescriptionText().toLowerCase().contains("git")) {
            tool.addTheme("Git");
        }
        if (tool.getDescription().toLowerCase().contains("ledger")) {
            tool.addTheme("Ledger");
        }
        if (tool.getDescription().toLowerCase().contains("time")) {
            tool.addTheme("Time");
        }
        if (tool.getDescription().toLowerCase().contains("mail")
                || tool.getDescription().toLowerCase().contains("smtp")) {
            tool.addTheme("Mail");
        }
    }
}