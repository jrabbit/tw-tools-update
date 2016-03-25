package org.brnvrn;

import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonToken;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.MappingJsonFactory;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jcabi.github.Github;
import com.jcabi.github.mock.MkGithub;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;

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
    public static void main(String[] args) throws IOException {

        JsonFactory f = new MappingJsonFactory();
        JsonParser jp = null;
        InputStream dataTools = null;
        try {
            ClassLoader classloader = Thread.currentThread().getContextClassLoader();
            dataTools = classloader.getResourceAsStream("data-tools.json");
            InputStream github1 = classloader.getResourceAsStream("github.1.100.json");
            jp = f.createParser(github1);
        } catch (IOException e) {
            e.printStackTrace();
        }

        ObjectMapper mapper = new ObjectMapper();
        List<Tool> tools = mapper.readValue(dataTools, new TypeReference<List<Tool>>() {});
        System.out.println("Loaded " + tools.size() +" old tools.");


        JsonToken current;
        current = jp.nextToken();
        if (current != JsonToken.START_OBJECT) {
            System.out.println("Error: root should be object: quiting.");
            return;
        }
        while (jp.nextToken() != JsonToken.END_OBJECT) {
            String fieldName = jp.getCurrentName();
            current = jp.nextToken();
            if (fieldName.equals("items")) {
                if (current == JsonToken.START_ARRAY) {
                    // For each of the item in the array
                    while (jp.nextToken() != JsonToken.END_ARRAY) {
                        // read the record into a tree model,
                        // this moves the parsing position to the end of it
                        JsonNode node = jp.readValueAsTree();
                        // And now we have random access to everything in the object
                        if (isToolUpdate(node, tools)) {
                            System.out.println("Updated name: " + node.get("full_name").asText());
                        } else {
                            addTools(node, tools);
                            System.out.println("Added name: " + node.get("full_name").asText());
                            System.out.println("description: " + node.get("description").asText());
                            System.out.println("Owner: " + node.get("owner").get("login").asText());
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

        // write the new updated data
        try {
            mapper.writeValue( new FileOutputStream("data-tools.json"), tools );
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Add a new tool to the list of existing tools
     *  Todo: Category???
     * @param node
     * @param tools
     */
    private static void addTools(JsonNode node, List<Tool> tools) {
        boolean isObsolete = false;
        Tool tool = new Tool(isObsolete);
        tool.setName(node.get("name").asText());
        tool.setDescription(node.get("description").asText());
        tool.addAuthor(node.get("owner").get("login").asText());
        // TODO complete
        tools.add(tool);
    }

    /**
     * Is the tool previously existing?  Then update and return yes
     * @param node
     * @param tools
     * @return
     */
    private static boolean isToolUpdate(JsonNode node, List<Tool> tools) {
        String name = node.get("name").asText();
        //tools.stream()
        return true;
    }
}