import com.hazelcast.config.Config;
import com.hazelcast.core.Hazelcast;
import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.map.IMap;
import com.hazelcast.client.HazelcastClient;
import java.util.Map;
import java.util.Queue;

public class Node {
    public static void main(String[] args) {
        Config cfg = new Config();
        HazelcastInstance hz = HazelcastClient.newHazelcastClient();
        IMap<Integer, String> distributedMap = hz.getMap( "myDistributedMap" );
        for (int i = 0; i < 1000; i++) {
            distributedMap.put(i, String.valueOf(i));
        }
        hz.shutdown();
    }
}
