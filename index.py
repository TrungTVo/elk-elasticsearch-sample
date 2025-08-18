from elasticsearch import Elasticsearch, helpers

client = Elasticsearch("http://localhost:9200")

index_name = "books"

def create_index(client, index_name):
    mappings = {
        "properties": {
            "title": {
                "type": "text"
            },
            "author": {
                "type": "text"
            },
            "description": {
                "type": "text"
            },
        }
    }

    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name)
        print(f"Index '{index_name}' does not exist. Creating index...")

    mapping_response = client.indices.put_mapping(index=index_name, body=mappings)
    print(mapping_response)


def delete_index(client, index_name):
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted.")


def bulk_insert():
    docs = [
        {
            "title": "Yellowstone",
            "description": "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site.",
            "author": "Trung Vo"
        },
        {
            "title": "Yosemite",
            "description": "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face.",
            "author": "Aiko Chu"
        },
        {
            "title": "Rocky Mountain",
            "description": "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site.",
            "author": "John Doe"
        }
    ]

    bulk_response = helpers.bulk(client, docs, index=index_name)
    print(bulk_response)


def text_search(text: str):
    response = client.esql.query(
        query=f"""FROM {index_name} | WHERE MATCH(description, "{text}") | LIMIT 5""",
        format="json"
    )

    print(response)


# create_index(client, index_name)
# delete_index(client, index_name)
# bulk_insert()
text_search("Yosemite")