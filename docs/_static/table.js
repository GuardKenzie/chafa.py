// Get all classes


function gen_td(element, id, type) {
    // Generate a
    a = document.createElement("a")
    a.classList.add("reference")
    a.classList.add("internal")

    a.href = `#${id}`

    // Generate code
    code = document.createElement("code")
    code.classList.add(
        "xref", 
        "py", 
        `py-${type}`, 
        "docutils", 
        "literal", 
        "notranslate"
    )

    code.appendChild(element)

    a.appendChild(code)

    // Generate td
    td = document.createElement("td")
    td.appendChild(a)
    
    return td
}


window.addEventListener("load", () => {
    const classes = document.querySelectorAll(".class")

    for (const c of classes) {

        const parent = c.parentElement;

        const members = {
            "properties": c.querySelectorAll('.property .sig'),
            "attributes": c.querySelectorAll('.attribute .sig'),
            "methods":    c.querySelectorAll('.method .sig')
        }

        // Figure out longest column
        const max_len = Math.max(
            members.properties.length,
            members.attributes.length,
            members.methods.length
        )
        
        // Gen table and fill table with empty td
        const empty_row = Array(Object.keys(members).length)
            .fill(0)
            .map(
                x => document.createElement("td")
            )
        
        // Init table
        const table = document.createElement("table")
        table.classList.add("class_contents")

        const table_header = Array(Object.keys(members).length)
            .fill(0)
            .map(
                x => document.createElement("th")
            )

        console.log(table_header)

        const table_rows = Array(max_len).fill(0).map(x => [...empty_row])
        
        for(let i = 0; i < members.properties.length; i++) {
            // Add header
            if (i == 0) {
                const properties_header = document.createElement("th")

                const properties_span = document.createElement("span")
                properties_span.classList.add("properties")

                properties_span.innerHTML = "Properties"
                properties_header.appendChild(properties_span)
    
                table_header[0] = properties_header
            }

            property = members.properties[i]

            // find name
            descname = property.querySelector(".descname .pre").cloneNode(true);

            // Generate td
            td = gen_td(descname, property.id, "prop")

            table_rows[i][0] = td
            
        }

        for(let i = 0; i < members.attributes.length; i++) {
            // Add header
            if (i == 0) {
                const attributes_header = document.createElement("th")

                const attributes_span = document.createElement("span")
                attributes_span.classList.add("attributes")

                attributes_span.innerHTML = "Attributes"
                attributes_header.appendChild(attributes_span)
    
                table_header[1] = attributes_header
            }

            attribute = members.attributes[i]

            // find name
            descname = attribute.querySelector(".descname").cloneNode(true);

            // Generate td
            td = gen_td(descname, attribute.id, "attr")

            table_rows[i][1] = td
        }

        

        for(let i = 0; i < members.methods.length; i++) {
            // Add header
            if (i == 0) {
                const methods_header = document.createElement("th")

                const methods_span = document.createElement("span")
                methods_span.classList.add("methods")

                methods_span.innerHTML = "Methods"
                methods_header.appendChild(methods_span)
    
                table_header[2] = methods_header
            }

            method = members.methods[i];

            // find name
            descname = method.querySelector(".descname").cloneNode(true);

            if (!descname.innerText.endsWith("]")) descname.innerText += "()"

            // Generate td
            td = gen_td(descname, method.id, "meth")

            table_rows[i][2] = td
            
        }

        

        // Create header
        header_row = document.createElement("tr")

        for (const header of table_header) {
            header_row.appendChild(header.cloneNode(true))
        }

        table.appendChild(header_row)

        for (let row of table_rows) {
            tr = document.createElement("tr")

            for (let td of row) {
                tr.appendChild(td.cloneNode(true))
            }

            table.appendChild(tr)
        }


        // Figure out where to put the table
        const class_contents = c.children[1].children;
        var before_element;
        var i = 0;

        while (i < class_contents.length) {
            before_element = class_contents[i]

            if (before_element.classList.contains("py")) break;

            i++;
        }

        c.children[1].insertBefore(table, before_element)
    }
})