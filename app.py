from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server

df = pd.read_excel('Vendas.xlsx', sheet_name="Sheet1")

vendas_por_categoria = df["Categoria"].value_counts().reset_index()
vendas_por_categoria.columns = ["Categoria", "Quantidade Vendidas"]

vendas_por_marca = df["Marca"].value_counts().reset_index()
vendas_por_marca.columns = ["Marca", "Qtd. Vendidas"]

media_preco_unitario = df.groupby("Produto")["PrecoUnitario"].mean().reset_index()

media = df["PrecoUnitario"].mean()

res = media_preco_unitario[media_preco_unitario["PrecoUnitario"] > media]

fig1 = px.bar(vendas_por_marca, x="Qtd. Vendidas", y="Marca", title="Vendas Por marca", template="plotly_dark")

fig1.update_layout(
   plot_bgcolor="#292929",
   paper_bgcolor="#292929"
  )

fig1.update_traces(
  marker_color="#d41414"
)

fig2 = px.pie(vendas_por_categoria, names="Categoria", values="Quantidade Vendidas", title="Vendas Por Categoria", template="plotly_dark", hole=0.5)

fig2.update_layout(
   plot_bgcolor="#292929",
   paper_bgcolor="#292929"
  )

fig2.update_traces(
   marker=dict(colors=["#ff0000","#d55513","#14137b","#f21068db","#267e2d","#edcc32db"])
  )

fig3 = px.bar(res, x="Produto", y="PrecoUnitario", title="Produtos Com Preco Unitario Acima Da Média", template="plotly_dark")

fig3.update_layout(
   plot_bgcolor="#292929",
   paper_bgcolor='#292929'
  )

fig3.update_traces(
   marker_color="#d41414"
  )

fig3.update_xaxes(
    tickvals=res["Produto"],
    ticktext=[p[:10] + "..." if len(p) > 10 else p for p in res["Produto"]]
)

app.layout = dbc.Container([
   dbc.Row([
     html.H1("Dashboard De vendas", style={"text-align": "center", "font-weight": "bold", "margin-bottom": "0.5rem"})
        ]),
      html.Hr(),
    
    dbc.Row([
      dbc.Col([
        dbc.Card([
         dbc.CardBody([
          html.H4("Faturamento Total", className="card-title"),
            html.H3("16 MILHÕES DE REAIS", style={"margin-bottom": "2.8rem"})
            ]),
    ],style={"width": "18rem"})
        ]),
        
      dbc.Col([
        dbc.Card([
         dbc.CardBody([
          html.H4("Produto Mais Vendido"),
            html.H3("Headphone Azultooth", style={"margin-bottom": "2.8rem"})
            ]),
    ],style={"width": "18rem"})
        ]),
        
      dbc.Col([
        dbc.Card([
         dbc.CardBody([
          html.H4("Produto com Maior Preço Unitário", style={"margin-bottom": "3.2rem"}),
          
          html.H3("Sistema de Som 7.1")
      ]),
    ],style={"width": "18rem"})
        ])
      ], style={"margin-bottom":"1.5rem"}),
    
    dbc.Row([
      dbc.Col([
        dcc.Graph(
          id="graf-bar",
          figure=fig1
          )
        ]),
        
      dbc.Col([
        dcc.Graph(
          id="graf-pizza",
          figure=fig2
          )
        ])
      ], style={"margin-bottom":"1.5rem"}),
      
    dbc.Row([
      dbc.Col([
         dcc.Graph(
           id="grafico-preco-unitario",
           figure=fig3
           )
        ])
      ])
  ], fluid=True)

if __name__ == "__main__":
  app.run(debug=True)
