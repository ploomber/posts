import sys
import nbformat
import pandas as pd 
import urllib.request
from string import Template

def convert(filename):

    print(f'Converting {filename} to PyScript dashboard')

    ref = nbformat.read(filename, as_version=nbformat.NO_CONVERT)
    cells = ref['cells']

    imports = []

    for cell in cells:
        if cell["cell_type"] == "code":
            tags = cell["metadata"].get("tags")
            source = cell["source"]

            # package imports
            if "import" in source:
                import_cells = source.replace("\n", "\n" + "    ")
                for package_import in source.split("\n"):
                    pkg = package_import.split(" ")[1]
                    if "." not in pkg and pkg != "urllib":
                        imports.append(f'"{pkg}"')
                    else:
                        main_pkg = pkg.split(".")[0]
                        if main_pkg != "urllib":
                            imports.append(f'"{main_pkg}"')

            if tags:

                for tag in tags:

                    # read data url
                    if "data-url" in tags:
                        data_url = source[source.find("=") + 1 :].strip().replace('"', "")

                    # data plot code
                    if "data-plot" in tags:
                        plot_code = source.replace("\n", "\n" + "        ")

                    if "filter" in tag:
                        filter_col_name = tag.split("-")[1]
                        filter_col = f'"{filter_col_name}"'
                        urllib.request.urlretrieve(data_url, filename="dataset.csv")
                        df = pd.read_csv("dataset.csv")
                        unique_filter_col_values = df[filter_col_name].unique().tolist()


    selection = f"Select {filter_col_name} : <br/>\n"
    selection += f"<input type=\"radio\" id=\"all\" name=\"{filter_col_name}\" value=\"ALL\">\n" 
    selection += "<label for=\"all\"> All</label>\n"

    for val in unique_filter_col_values:
        selection += f"<input type=\"radio\" id=\"{val}\" name=\"{filter_col_name}\" value=\"{val}\">\n" 
        selection += f"<label for=\"{val}\"> {val} </label>\n"


    template = Template(
        """<html> 
         <head> 
         <title>YouTube and Spotify artists</title>
         <meta charset="utf-8">
         <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
         <script defer src="https://pyscript.net/latest/pyscript.js"></script>
         </head>
         <body>
         <py-config> 
             packages = [ $packages ]
         </py-config>
         <py-script>
             
             $user_imports
             
             from pyodide.http import open_url
             from pyodide.ffi import create_proxy
             
             url = $url
             df = pd.read_csv(open_url(url))
             
             current_selected = []
             filter_elements = js.document.getElementsByName( $filter_column )
             
             def plot(df):
                 plt.rcParams["figure.figsize"] = (15, 10)
                 $code
                 display(fig, target="graph-area", append=False)
                 
             def select_filter(event):
                for ele in filter_elements:
                  if ele.checked:
                      current_selected = ele.value
                      break
                if current_selected == "ALL":
                  plot(df)
                else:
                  filter = df.apply(lambda x: ele.value in x[ $filter_column ], axis=1)
                  plot(df[filter])
                  
             ele_proxy = create_proxy(select_filter)
             
             for ele in filter_elements:
              if ele.value == "ALL":
                ele.checked = True
                current_selected = ele.value
              ele.addEventListener("change", ele_proxy)
             
             plot(df)
            
         </py-script>
         
         <div id="input" style="margin: 20px;">
          $selection

         </div>

        <py-repl>
          df
        </py-repl>

        <div id="graph-area"></div>
        
         </body>
         </html>
          """
    )


    dashboard = template.substitute(packages=(", ".join(imports)), 
                         url=f"\"{data_url}\"",
                         user_imports=import_cells,
                         code=plot_code,
                         filter_column=filter_col,
                         selection=selection)

    with open("dashboard.html", "w") as file:
        file.write(dashboard)


if __name__ == "__main__":
    notebook = sys.argv[1]
    convert(notebook)

