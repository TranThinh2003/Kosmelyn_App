from flet import *

class FilterView(Container):
    def __init__(self, on_filter_change_ui):
        if not callable(on_filter_change_ui):
            raise TypeError("on_filter_change_ui must be callable")
        super().__init__(padding=Padding(0, 10, 0, 10))

        self.all_prod = []
        self.on_filter_change_ui = on_filter_change_ui
        self.brand_filter_dd = Dropdown(
            options=[dropdown.Option("All Brands")],
            value ="All Brands",
            on_change=self._handle_filter_change,
            expand=True
        )

        self.price_filter_dd = Dropdown(
            options =[dropdown.Option("All Prices"), 
                      dropdown.Option("Low to High"), 
                      dropdown.Option("High to Low")],
            value ="All Prices",
            on_change=self._handle_filter_change,
            expand=True
        )

        self.skinType_filter_dd = Dropdown(
            options = [dropdown.Option("All Skin Types"),
                       dropdown.Option("Oily"),
                       dropdown.Option("Dry"),
                       dropdown.Option("Combination"),
                       dropdown.Option("Normal")],
            value = "All Skin Types",
            on_change=self._handle_filter_change,
            expand=True
        )

        self.content = Row(
            controls=[
                Text("Filter By:", size=16, color="black"),
                self.brand_filter_dd,
                self.price_filter_dd,
                self.skinType_filter_dd
            ],
            alignment=MainAxisAlignment.START,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )

    def _handle_filter_change(self,e=None):
        filtered_and_SortedList = self.apply_filters()
        self.on_filter_change_ui(filtered_and_SortedList)
    

    def update_data_and_options(self,prod_list):
        self.all_prod = prod_list
        
        unique_brand = sorted(set(p.get('Brand','N/A') for p in prod_list))
        brand_options = [dropdown.Option("All Brands")] + [dropdown.Option(brand) for brand in unique_brand]
        
        self.brand_filter_dd.options = brand_options
        self.brand_filter_dd.value = "All Brands"
        self.page.update()

        self.price_filter_dd.value = "All Prices"
        self.page.update()
        self.skinType_filter_dd.value = "All Skin Types"
        self.page.update()        

    def apply_filters(self):
        filtered_results = self.all_prod.copy()
        
        selected_brand = self.brand_filter_dd.value

        if selected_brand and selected_brand != "All Brands":
            filtered_results = [p for p in filtered_results if p.get('Brand','N/A') == selected_brand]
        
        sort_order = self.price_filter_dd.value
        
        if sort_order != "All Prices":
            def get_price(price):
                try:
                    price_str = price.get('Price','').replace('$','').replace(',','').strip()
                    return float(price_str)
                except (ValueError, AttributeError):
                    return float('inf') if sort_order == "Low to High" else -1

            reversed_order = (sort_order == "High to Low") 
            filtered_results.sort(key=get_price, reverse=reversed_order)

        if self.skinType_filter_dd.value and self.skinType_filter_dd.value != "All Skin Types":
            selected_skin_type = self.skinType_filter_dd.value
            filtered_results = [
                p for p in filtered_results 
                if selected_skin_type in p.get('Skin_Type', [])
            ]

        return filtered_results


