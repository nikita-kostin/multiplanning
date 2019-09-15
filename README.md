# multiplanning

Пример входного файла:

{
  "map": {
    "width": 3,
    "height": 5,
    "grid": [
      ["*", ".", "*"],
      ["*", ".", "*"],
      [".", ".", "*"],
      ["*", ".", "."],
      ["*", ".", "*"]
    ],
    "searches": [
      {
        "start": {
          "i": 0,
          "j": 1
        },
        "goal": {
          "i": 4,
          "j": 1
        }
      },
      {
        "start": {
          "i": 4,
          "j": 1
        },
        "goal": {
          "i": 0,
          "j": 1
        }
      }
    ]
  },
  "options": {
    "searchtype": "astar",
    "metrictype": "euclidean"
  }
}

Пример выходного файла:

{
  "search_results": [
    {
      "hppath": [
        {
          "i": 0,
          "j": 1,
          "t": 0
        },
        {
          "i": 4,
          "j": 1,
          "t": 4
        }
      ],
      "lppath": [
        {
          "i": 0,
          "j": 1,
          "t": 0
        },
        {
          "i": 1,
          "j": 1,
          "t": 1
        },
        {
          "i": 2,
          "j": 1,
          "t": 2
        },
        {
          "i": 3,
          "j": 1,
          "t": 3
        },
        {
          "i": 4,
          "j": 1,
          "t": 4
        }
      ],
      "numberofsteps": 18,
      "pathfound": true,
      "pathlength": 5,
      "pathlength_scaled": 5,
      "pathtime": 5,
      "time": 0.001591
    },
    {
      "hppath": [
        {
          "i": 4,
          "j": 1,
          "t": 0
        },
        {
          "i": 3,
          "j": 1,
          "t": 2
        },
        {
          "i": 3,
          "j": 2,
          "t": 3
        },
        {
          "i": 3,
          "j": 1,
          "t": 4
        },
        {
          "i": 0,
          "j": 1,
          "t": 7
        }
      ],
      "lppath": [
        {
          "i": 4,
          "j": 1,
          "t": 0
        },
        {
          "i": 4,
          "j": 1,
          "t": 1
        },
        {
          "i": 3,
          "j": 1,
          "t": 2
        },
        {
          "i": 3,
          "j": 2,
          "t": 3
        },
        {
          "i": 3,
          "j": 1,
          "t": 4
        },
        {
          "i": 2,
          "j": 1,
          "t": 5
        },
        {
          "i": 1,
          "j": 1,
          "t": 6
        },
        {
          "i": 0,
          "j": 1,
          "t": 7
        }
      ],
      "numberofsteps": 21,
      "pathfound": true,
      "pathlength": 6,
      "pathlength_scaled": 6,
      "pathtime": 8,
      "time": 0.001086
    }
  ]
}

В консоль частично выводится сагрегированная информация
Плюс создается GIF-файл, наглядно отображающий постоенные пути
